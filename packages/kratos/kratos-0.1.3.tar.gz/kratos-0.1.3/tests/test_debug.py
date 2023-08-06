from kratos import Generator, always_ff, verilog, posedge, always_comb, const
from kratos.util import reduce_add
import tempfile
import os
import json


def get_line_num(txt):
    with open(__file__) as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.strip() == txt:
            return i + 1
    return 0


def test_debug_fn_ln():
    class Mod(Generator):
        def __init__(self):
            super().__init__("mod1", True)
            self.in_ = self.input("in", 1)
            self.out_1 = self.output("out1", 1)
            self.out_2 = self.output("out2", 1)

            self.wire(self.out_1, self.in_)

            self.add_always(self.code)

        @always_comb
        def code(self):
            self.out_2 = self.in_

    mod = Mod()
    mod_src, mod_debug = verilog(mod, debug_fn_ln=True)
    src_mapping = mod_debug["mod1"]
    assert len(src_mapping) == 7
    verilog_lines = mod_src["mod1"].split("\n")
    verilog_ln = 0
    for ln, line in enumerate(verilog_lines):
        if "assign out1 = in;" in line:
            verilog_ln = ln + 1
            break
    fn, ln = src_mapping[verilog_ln][0]
    with open(fn) as f:
        python_lns = f.readlines()
    assert "self.wire(self.out_1, self.in_)" in python_lns[ln - 1]


def test_ssa_transform(check_gold):
    mod = Generator("mod", debug=True)
    a = mod.var("a", 4)
    b = mod.var("b", 4)
    c = mod.output("c", 4)

    @always_comb
    def func():
        a = 1
        a = 2
        if a == 2:
            a = b + a
        if a == 3:
            b = 2
        else:
            if a == 4:
                b = 3
            else:
                b = 4
                # this is not a latch
                a = 5
        c = a

    mod.add_always(func, ssa_transform=True)
    check_gold(mod, "test_ssa_transform", ssa_transform=True)
    # check if the local variable mapping is fixed
    # assign a_5 = (a_3 == 4'h4) ? a_3: a_4;
    # which corresponds to a = 5
    # notice that a should be pointing to a = b + a, since it's the last
    # time a gets assigned
    stmt = mod.get_stmt_by_index(3)[3]
    scope = stmt.scope_context
    is_var, a_mapping = scope["a"]
    assert is_var
    # this is assign a_2 = b + a_1;
    stmt = mod.get_stmt_by_index(3)[2]
    assert str(a_mapping) == str(stmt.left)

    # test enable table extraction
    from _kratos.passes import compute_enable_condition
    enable_map = compute_enable_condition(mod.internal_generator)
    assert len(enable_map) > 5


def test_enable_condition_always_ff():
    mod = Generator("mod")
    a = mod.var("a", 4)
    b = mod.var("b", 1)
    clk = mod.clock("clk")

    @always_ff((posedge, clk))
    def logic():
        if b:
            a = 0
        else:
            a = 1

    mod.add_always(logic)
    from _kratos.passes import compute_enable_condition
    enable_map = compute_enable_condition(mod.internal_generator)
    assert len(enable_map) == 2


def test_verilog_ln_fix():
    from kratos.func import dpi_function

    @dpi_function(8)
    def add(arg0, arg1):
        pass

    class Mod(Generator):
        def __init__(self):
            super().__init__("mod", debug=True)
            self._in = self.input("in", 2)
            self._out = self.output("out", 8)
            self.add_always(self.code)

        @always_comb
        def code(self):
            self._out = add(self._in, const(1, 2))
            if self._in == 0:
                self._out = 1

    mod = Mod()
    with tempfile.TemporaryDirectory() as temp:
        filename = os.path.join(temp, "test.sv")
        src = verilog(mod, filename=filename)[0]
        content = src["mod"]

    mod_i = mod.internal_generator
    assert mod_i.verilog_ln == 2
    lines = content.split("\n")
    stmt_0 = min([i for i in range(len(lines)) if "add (" in lines[i]])
    stmt_1 = min([i for i in range(len(lines)) if "if" in lines[i]])
    # + 1 for using starting-1 line number format
    # another + 1 for DPI header offset
    assert mod.get_stmt_by_index(0)[0].verilog_ln == stmt_0 + 1 + 1
    assert mod.get_stmt_by_index(0)[1].then_body().verilog_ln == stmt_1 + 2


def test_db_dump():
    mod = Generator("mod", True)
    comb = mod.combinational()
    comb.add_stmt(mod.var("a", 1).assign(mod.var("b", 1)))

    with tempfile.TemporaryDirectory() as temp:
        debug_db = os.path.join(temp, "debug.db")
        # hashing and generate verilog
        verilog(mod, insert_debug_info=True, debug_db_filename=debug_db)
        with open(debug_db) as f:
            db = json.load(f)
    assert db["generator"] == "kratos"
    assert db["top"] == mod.name
    mod_def = db["table"][0]
    assert mod_def["name"] == mod.name
    assert len(mod_def["scope"]) == 1
    comb = mod_def["scope"][0]
    assert comb["filename"] == __file__
    assert len(comb["scope"]) == 1
    assign = comb["scope"][0]
    ref_line = get_line_num('comb.add_stmt(mod.var("a", 1).assign(mod.var("b", 1)))')
    assert assign["line"] == ref_line
    var = assign["variable"]
    assert var["name"] == "a"


def test_debug_mock():
    # this is used for the runtime debugging
    class Mod(Generator):
        def __init__(self):
            super().__init__("mod", True)

            # ports
            self.in1 = self.input("in1", 16)
            self.in2 = self.input("in2", 16)
            self.out = self.output("out", 16)

            self.add_always(self.code)

        @always_comb
        def code(self):
            if self.in1 == 2:
                self.out = 2
            elif self.in1 == 1:
                self.out = 0
            elif self.in2 == 1:
                self.out = 1
            else:
                self.out = 3

    with tempfile.TemporaryDirectory() as temp:
        mod = Mod()
        debug_db = os.path.join(temp, "debug.db")
        filename = os.path.join(temp, "test.sv")
        verilog(mod, filename=filename, insert_debug_info=True,
                insert_verilator_info=True, debug_db_filename=debug_db)
        # make sure the verilator public is there
        with open(filename) as f:
            content = f.read()
        assert "verilator public" in content


def test_seq_debug():
    class Mod(Generator):
        def __init__(self):
            super().__init__("mod", True)
            # ports
            self.in_ = self.input("in1", 1)
            self.clock("clk")
            for i in range(4):
                self.output("out{0}".format(i), 1)

            self.add_always(self.code1)
            self.add_always(self.code2)

        @always_comb
        def code1(self):
            if self.in_ == 0:
                self.ports.out0 = 0
                self.ports.out1 = 0
            else:
                self.ports.out0 = 1
                self.ports.out1 = 1

        @always_ff((posedge, "clk"))
        def code2(self):
            if self.in_ == 0:
                self.ports.out2 = 0
                self.ports.out3 = 0
            else:
                self.ports.out2 = 1
                self.ports.out3 = 1

    mod = Mod()
    with tempfile.TemporaryDirectory() as temp:
        debug_db = os.path.join(temp, "debug.db")
        filename = os.path.join(temp, "test.sv")
        verilog(mod, filename=filename, insert_debug_info=True,
                debug_db_filename=debug_db)
        with open(debug_db) as f:
            db = json.load(f)
    # it should have two scopes
    mod_db = db["table"][0]
    assert mod_db["name"] == mod.name
    scopes = mod_db["scope"]
    assert len(scopes) == 2
    variables = {}
    for v in db["variables"]:
        variables[v["id"]] = v
    for i in range(2):
        code = scopes[i]
        decl = code["scope"][0]
        assert decl["type"] == "decl"
        var = db["variables"][-1]
        # this one is i, which should be compressed
        v_id = decl["variable"]
        assert v_id in variables
        var = variables[v_id]
        assert var["name"] == "i"
        assert var["value"] == "3"
        if_stmt = code["scope"][1]
        assert len(if_stmt["scope"]) == 2
        for stmt in if_stmt["scope"]:
            assert len(stmt["scope"]) == 2
            # two assignments
            for a in stmt["scope"]:
                assert a["type"] == "assign"
    # test out gen var
    assert len(mod_db["variables"]) == 1
    assert mod_db["variables"][0]["name"] == "self.in_"


def test_context():
    class Mod(Generator):
        def __init__(self, width):
            super().__init__("mod", debug=True)
            in_ = self.input("in", width)
            out = self.output("out", width)
            sel = self.input("sel", width)
            # test self variables
            self.out = out
            self.width = width

            @always_comb
            def code():
                if sel:
                    out = 0
                else:
                    for i in range(width):
                        out[i] = 1
            self.add_always(code)

    w = 4
    mod = Mod(w)
    with tempfile.TemporaryDirectory() as temp:
        debug_db = os.path.join(temp, "debug.db")
        filename = os.path.join(temp, "test.sv")
        verilog(mod, filename=filename, insert_debug_info=True,
                debug_db_filename=debug_db)
        with open(debug_db) as f:
            db = json.load(f)
        mod_db = db["table"][0]
        code = mod_db["scope"][-1]
        else_blk = code["scope"][-1]["scope"][-1]["scope"]
        assert len(else_blk) == (w * 2)
        values = set()
        for entry in else_blk:
            if entry["type"] == "decl" and entry["variable"]["name"] == "i":
                values.add(int(entry["variable"]["value"]))
        for i in range(w):
            assert i in values


def test_clock_interaction():
    mods = []
    num_child = 4
    for i in range(num_child):
        mod = Generator("mod", True)
        in_ = mod.input("in", 4)
        out_ = mod.output("out", 4)
        clk = mod.clock("clk")
        seq = mod.sequential((posedge, clk))
        seq.add_stmt(out_.assign(in_))
        mods.append(mod)
    parent = Generator("parent", True)
    clk = parent.clock("clk")
    in_ = parent.input("in", 4)
    out = parent.output("out", 4)
    for i, mod in enumerate(mods):
        parent.add_child("mod{0}".format(i), mod)
        parent.wire(mod.ports.clk, clk)
        if i == 0:
            continue
        parent.wire(mod.ports["in"], mods[i - 1].ports.out)
    parent.wire(mods[0].ports["in"], in_)
    parent.wire(out, mods[-1].ports.out)
    with tempfile.TemporaryDirectory() as temp:
        debug_db = os.path.join(temp, "debug.db")
        filename = os.path.join(temp, "test.sv")
        verilog(parent, filename=filename, insert_debug_info=True,
                debug_db_filename=debug_db)


def test_assert_fail(check_gold):
    import _kratos
    from kratos import initial, assert_
    mod = Generator("gen", debug=True)
    a = mod.var("a", 1)

    @initial
    def code():
        assert_(a)  # mark 1

    mod.add_always(code)
    assert_stmt = mod.get_stmt_by_index(0)[0]
    assert isinstance(assert_stmt, _kratos.AssertValueStmt)
    assert_stmt.fn_name_ln = [("test.py", 42)]

    check_gold(mod, "test_assert_fail", insert_debug_info=True)


def test_wire():
    mod = Generator("mod", True)
    in_ = mod.input("in", 1)
    out_ = mod.output("out", 1)
    # context
    a = 1
    mod.wire(out_, in_)
    with tempfile.TemporaryDirectory() as temp:
        debug_db = os.path.join(temp, "debug.db")
        filename = os.path.join(temp, "test.sv")
        verilog(mod, filename=filename, insert_debug_info=True,
                debug_db_filename=debug_db)
        with open(debug_db) as f:
            db = json.load(f)
        assign = db["table"][0]["scope"][0]["scope"][-1]
        assert assign["type"] == "assign"
        assert assign["variable"]["name"] == "out"
        line = get_line_num("mod.wire(out_, in_)")
        assert assign["line"] == line


def test_multiple_definitions():
    def create_mod(idx):
        m = Generator("mod" + str(idx), True)
        in_ = m.input("in", 1)
        out = m.output("out", 1)
        comb = m.combinational()
        comb.add_stmt(out.assign(in_))
        return m
    mod = Generator("parent", True)
    input_ = mod.input("in", 1)
    output = mod.output("out", 1)
    mods = [create_mod(i) for i in range(2)]
    expr = None
    for i, m_ in enumerate(mods):
        mod.add_child("mod{0}".format(i), m_)
        mod.wire(input_, m_.ports["in"])
        if expr is None:
            expr = m_.ports["out"]
        else:
            expr = expr & m_.ports["out"]
    mod.wire(output, expr)

    with tempfile.TemporaryDirectory() as temp:
        debug_db = os.path.join(temp, "debug.db")
        verilog(mod, insert_debug_info=True, debug_db_filename=debug_db,
                optimize_passthrough=False)
        with open(debug_db) as f:
            db = json.load(f)
        assert len(db["table"]) == 3


def test_empty():
    from kratos.debug import dump_external_database
    mod = Generator("mod", True)
    with tempfile.TemporaryDirectory() as temp:
        debug_db = os.path.join(temp, "debug.db")
        dump_external_database([mod], "mod", debug_db)


def test_nested_scope():
    from kratos import clog2
    mod = Generator("FindHighestBit", True)
    width = 4
    data = mod.input("data", width)
    h_bit = mod.output("h_bit", clog2(width))
    done = mod.var("done", 1)

    @always_comb
    def find_bit():
        done = 0
        h_bit = 0
        for i in range(width):
            if ~done:
                if data[i]:
                    done = 1
                    h_bit = i
    mod.add_always(find_bit, label="block")
    verilog(mod, insert_debug_info=True)
    block = mod.get_marked_stmt("block")
    last_if = block[-1]
    for i in range(len(last_if.then_[-1].then_)):
        stmt = last_if.then_[-1].then_[i]
        context = stmt.scope_context
        if len(context) > 0:
            assert "i" in context
            is_var, var = context["i"]
            assert not is_var
            assert var == "3"


def test_array_packed():
    from kratos import PackedStruct
    mod = Generator("mod", True)
    aa = mod.var("a", 2, size=(2, 4), packed=True)
    struct = PackedStruct("s", [("read", 16, False),
                                ("data", 16, False)])
    ss = mod.var_packed("s", struct)
    mod.add_stmt(aa.assign(4))
    setattr(mod, "sss", ss)
    mod.add_stmt(ss["read"].assign(0))
    mod.add_stmt(ss["data"].assign(1))

    with tempfile.TemporaryDirectory() as temp:
        debug_db = os.path.join(temp, "debug.db")
        verilog(mod, debug_db_filename=debug_db, insert_debug_info=True)
        with open(debug_db) as f:
            db = json.load(f)
    mod_db = db["table"][0]
    mod_variables = mod_db["variables"]
    assert len(mod_variables) == 2
    assert mod_variables[0]["name"] == "self.sss.read"
    assert mod_variables[1]["name"] == "self.sss.data"
    assert mod_variables[0]["value"] == "s.read"
    assert mod_variables[1]["value"] == "s.data"

    first_assign = mod_db["scope"][0]
    names = set()
    values = set()
    for entry in first_assign["scope"]:
        if entry["type"] == "assign":
            var = entry["variable"]
            names.add(var["name"])
            values.add(var["value"])

    for i in range(4):
        for j in range(2):
            name = "a.{0}.{1}".format(j, i)
            value = "a[{0}][{1}]".format(j, i)
            assert name in names
            assert value in values


def test_multiple_instance():
    class Mod(Generator):
        def __init__(self, width, param):
            super().__init__("child_{0}_{1}".format(width, param), True)
            in_ = self.input("child_in", width)
            out_ = self.output("child_out", width)

            @always_comb
            def code():
                out_ = 0
                for i in range(param):
                    out_ = in_ + param

            self.add_always(code)

    top = Generator("parent", True)
    top_in = top.input("in", 8)
    top_out = top.output("out", 8)
    children = []
    out_ports = []
    num_instance = 3
    for i in range(num_instance):
        child = Mod(8, i + 2)
        children.append(child)
    for i in range(num_instance):
        child = children[i]
        top.add_child("child_{0}".format(i), child,
                      child_in=top_in)
        out_ports.append(child.ports.child_out)

    top.wire(top_out, reduce_add(*out_ports))

    # testing code
    with tempfile.TemporaryDirectory() as temp:
        filename = os.path.join(temp, "test.sv")
        verilog(top, filename=filename, insert_debug_info=True, debug_fn_ln=True)
        # make sure that the line is mapped correctly
        with open(__file__) as f:
            lines = f.readlines()
            index = -1
            for i in range(len(lines)):
                if "out_ = in_ + param" in lines[i]:
                    index = i
                    break
            assert index != -1
        line_no = index + 1  # 1 offset for line number
        with open(filename + ".debug") as f:
            import json
            content = json.load(f)
        count = 0
        for _, entry in content.items():
            __, ln = entry[0]
            if ln == line_no:
                count += 1
        assert count == num_instance * (num_instance + 3) / 2


def test_ssa_debug():
    mod = Generator("mod", debug=True)
    a = mod.var("a", 4)
    clk = mod.clock("clk")
    b = mod.var("b", 1)
    loop_size = 4

    @always_comb
    def logic1():
        a = 0
        if b:
            for i in range(loop_size):
                a = a + i

    @always_ff((posedge, clk))
    def logic2():
        if a == 1:
            b = 1
        else:
            b = 0   # test_ssa_debug

    mod.add_always(logic1, ssa_transform=True)
    mod.add_always(logic2)

    with tempfile.TemporaryDirectory() as temp:
        debug_db = os.path.join(temp, "debug.db")
        verilog(mod, insert_debug_info=True, debug_db_filename=debug_db, ssa_transform=True)
        with open(debug_db) as f:
            db = json.load(f)
    mod_db = db["table"][0]
    logic1_db = mod_db["scope"][0]["scope"]
    assert len(logic1_db) == (4 + 2 * (loop_size + 1))
    # a_0 = 0
    # 4x (a_i + i)
    idx = 0
    for entry in logic1_db[4:13]:
        var = entry["variable"]
        name = var["name"]
        value = var["value"]
        if name == "i":
            assert value == str(idx)
            idx += 1
        else:
            assert name == "a"
            assert value == "a_{0}".format(idx)
    # enable conditions
    line = get_line_num("b = 0   # test_ssa_debug")
    logic2_db = mod_db["scope"][1]["scope"]
    last_assign = logic2_db[-1]["scope"][-1]["scope"][0]
    assert last_assign["type"] == "assign"
    assert last_assign["condition"] == "!(a == 4'h1)"
    assert last_assign["line"] == line


def test_assign_slice():
    mod = Generator("mod", debug=True)
    a = mod.var("a", 16, size=[2])
    b = mod.input("b", 1)
    c = mod.input("c", 16)
    mod.wire(c, a[b])

    with tempfile.TemporaryDirectory() as temp:
        debug_db = os.path.join(temp, "debug.db")
        verilog(mod, insert_debug_info=True, debug_db_filename=debug_db)
        with open(debug_db) as f:
            db = json.load(f)
    mod_db = db["table"][0]
    assert mod_db["name"] == "mod"
    assigns = mod_db["scope"][0]["scope"][3:]
    assert len(assigns) == 2
    for i in range(2):
        assert assigns[i]["variable"]["name"] == "a.{0}".format(i)
        assert assigns[i]["variable"]["value"] == "a[{0}]".format(i)


if __name__ == "__main__":
    test_verilog_ln_fix()
