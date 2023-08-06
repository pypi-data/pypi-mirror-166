#include "codegen.hh"

#include <fmt/format.h>

#include <mutex>

#include "context.hh"
#include "cxxpool.h"
#include "except.hh"
#include "expr.hh"
#include "generator.hh"
#include "graph.hh"
#include "interface.hh"
#include "pass.hh"
#include "tb.hh"
#include "util.hh"

using fmt::format;

namespace kratos {

std::string get_var_size_str(Var* var);

Stream::Stream(Generator* generator, SystemVerilogCodeGen* codegen)
    : generator_(generator), codegen_(codegen), line_no_(1) {}

Stream& Stream::operator<<(AssignStmt* stmt) {
    const auto left = var_str(stmt->left());
    const auto right = var_str(stmt->right());
    if (!stmt->comment.empty()) {
        (*this) << "// " << strip_newline(stmt->comment) << endl();
        (*this) << codegen_->indent();
    }

    if (generator_->debug) {
        stmt->verilog_ln = line_no_;
    }

    std::string prefix;
    std::string eq;

    if (stmt->parent() == generator_) {
        // top level
        if (stmt->assign_type() != AssignmentType::Blocking)
            throw StmtException(
                ::format("Top level assignment for {0} <- {1} has to be blocking", left, right),
                {stmt->left(), stmt->right(), stmt});
        if (stmt->has_delay()) {
            throw StmtException("Continuous assignment cannot have delay", {stmt});
        }
        prefix = "assign ";
        eq = "=";
    } else {
        prefix = codegen_->indent();
        if (stmt->assign_type() == AssignmentType::Blocking)
            eq = "=";
        else if (stmt->assign_type() == AssignmentType::NonBlocking)
            eq = "<=";
        else
            throw StmtException(
                ::format("Top level assignment for {0} <- {1} has to be blocking", left, right),
                {stmt->left(), stmt->right(), stmt});
    }

    (*this) << prefix;
    auto var_str_func = [this](const Var* v) { return var_str(v); };
    auto output_delay = [this, &var_str_func](const EventControl& e) {
        switch (e.type) {
            case EventControlType::Delay: {
                (*this) << e.to_string(var_str_func) << ' ';
                break;
            }
            case EventControlType::Edge: {
                (*this) << "@(" << e.to_string(var_str_func) << ") ";
            }
        }
    };
    // lhs delay
    if (stmt->has_delay() && stmt->get_delay()->delay_side == EventControl::DelaySide::left) {
        // this is a lhs delay
        output_delay(*stmt->get_delay());
    }

    (*this) << left << " " << eq << " ";  //<< right << ";" << endl();

    // rhs delay
    if (stmt->has_delay() && stmt->get_delay()->delay_side == EventControl::DelaySide::right) {
        // this is a rhs delay
        output_delay(*stmt->get_delay());
    }

    auto right_wrapped = line_wrap(right, codegen_->options().line_wrap);
    (*this) << right_wrapped[0];
    for (uint64_t i = 1; i < right_wrapped.size(); i++) {
        // compute new indent
        (*this) << endl();
        (*this) << codegen_->indent() << "    " << right_wrapped[i];
    }
    (*this) << ";" << endl();
    return *this;
}

Stream& Stream::operator<<(const std::pair<Port*, std::string>& port) {
    const auto& [p, end] = port;
    if (!p->comment.empty())
        (*this) << codegen_->indent() << "// " << strip_newline(p->comment) << endl();
    if (generator_->debug) {
        p->verilog_ln = line_no_;
    }

    (*this) << codegen_->indent() << p->before_var_str() << SystemVerilogCodeGen::get_port_str(p)
            << p->after_var_str() << end << endl();

    return *this;
}

std::string Stream::get_var_decl(kratos::Var* var) {
    // based on whether it's packed or not
    std::string type;
    if (var->is_struct()) {
        auto v = var->as<VarPackedStruct>();
        type = v->packed_struct()->struct_name;
    } else if (var->is_enum()) {
        auto* v = dynamic_cast<EnumType*>(var);
        if (!v) throw InternalException("Unable to resolve var to enum type");
        type = v->enum_type()->name;
    } else {
        type = "logic";
    }

    std::vector<std::string> str = {type};
    if (var->is_signed()) str.emplace_back("signed");
    std::string var_width = SystemVerilogCodeGen::get_var_width_str(var);
    if (var->size().front() > 1 || var->size().size() > 1 || var->explicit_array()) {
        // it's an array
        if (var->is_packed()) {
            std::string array_str = get_var_size_str(var);
            if (!var_width.empty()) array_str.append(var_width);
            str.emplace_back(array_str);
            str.emplace_back(var->name);
        } else {
            if (!var_width.empty()) str.emplace_back(var_width);
            str.emplace_back(var->name);
            std::string array_str = get_var_size_str(var);
            str.emplace_back(array_str);
        }
    } else {
        // scalar
        if (!var_width.empty() && !var->is_enum()) str.emplace_back(var_width);
        str.emplace_back(var->name);
    }

    auto var_str = string::join(str.begin(), str.end(), " ");
    return var_str;
}

Stream& Stream::operator<<(const std::shared_ptr<Var>& var) {
    if (!var->comment.empty()) (*this) << "// " << strip_newline(var->comment) << endl();

    if (generator_->debug) {
        var->verilog_ln = line_no_;
    }

    auto var_str = get_var_decl(var.get());

    (*this) << var->before_var_str() << var_str << var->after_var_str() << ";" << endl();
    return *this;
}

std::string Stream::var_str(const kratos::Var* var) const {
    if (var->generator() == generator_ || var->generator() == Const::const_gen())
        return var->to_string();
    else
        return var->handle_name(true);
}

std::string Stream::var_str(const std::shared_ptr<Var>& var) const { return var_str(var.get()); }

void VerilogModule::run_passes() {
    // run multiple passes using pass manager
    // run the passes
    manager_.run_passes(generator_);
}

std::map<std::string, std::string> VerilogModule::verilog_src() {
    return generate_verilog(generator_, {});
}

std::map<std::string, std::string> VerilogModule::verilog_src(SystemVerilogCodeGenOptions options) {
    return generate_verilog(generator_, options);
}

SystemVerilogCodeGen::SystemVerilogCodeGen(Generator* generator)
    : SystemVerilogCodeGen(generator, {}) {}

SystemVerilogCodeGen::SystemVerilogCodeGen(kratos::Generator* generator,
                                           SystemVerilogCodeGenOptions options)
    : generator_(generator), options_(std::move(options)), stream_(generator, this) {
    // if it's an external file, we don't output anything
    if (generator->external()) return;

    // index the named blocks
    label_index_ = index_named_block();

    // check if we need to inline src attribute with yosys
    check_yosys_src();
}

void SystemVerilogCodeGen::check_yosys_src() {
    for (auto const& attr : generator_->get_attributes()) {
        if (attr->value_str == "yosys_src") {
            options_.yosys_src = true;
        }
    }
}

void SystemVerilogCodeGen::output_module_def(Generator* generator) {  // output module definition
    // insert the header definition, if necessary
    if (!options_.package_name.empty()) {
        // two line indent
        stream_ << "`include \"" << options_.package_name << ".svh\"" << stream_.endl()
                << stream_.endl();
        // import everything
        stream_ << "import " << options_.package_name << "::*;" << stream_.endl();
    }
    if (generator->debug) generator->verilog_ln = stream_.line_no();
    stream_ << ::format("module {0} ", generator->name);
    generate_module_package_import(generator);
    generate_parameters(generator);
    stream_ << indent() << "(" << stream_.endl();
    generate_ports(generator);
    stream_ << indent() << ");" << stream_.endl() << stream_.endl();
    generate_enums(generator);
    generate_variables(generator);
    generate_interface(generator);
    generate_functions(generator);

    for (uint64_t i = 0; i < generator->stmts_count(); i++) {
        dispatch_node(generator->get_stmt(i).get());
    }

    stream_ << ::format("endmodule   // {0}", generator->name) << stream_.endl();
}

void SystemVerilogCodeGen::generate_module_package_import(Generator* generator) {
    auto const& raw_import = generator->raw_package_imports();
    if (raw_import.empty()) return;
    stream_ << stream_.endl();
    indent_++;
    for (auto const& pkg_name : raw_import) {
        stream_ << indent() << "import " << pkg_name << "::*;" << stream_.endl();
    }
    indent_--;
}

std::string SystemVerilogCodeGen::get_var_width_str(const Var* var) {
    std::string width;
    if (var->parametrized()) {
        width = ::format("{0}-1", var->width_param()->to_string());
    } else {
        width = std::to_string(var->var_width() - 1);
    }
    return (var->var_width() > 1 && !var->is_struct()) || var->parametrized()
               ? ::format("[{0}:0]", width)
               : "";
}

std::string SystemVerilogCodeGen::get_width_str(uint32_t width) {
    return ::format("[{0}:0]", width - 1);
}

std::string SystemVerilogCodeGen::get_width_str(Var* var) {
    std::string format;
    if (var->type() == VarType::Parameter)
        format = "[{0}-1:0]";
    else
        format = "[({0})-1:0]";
    return ::format(format.c_str(), var->to_string());
}

void SystemVerilogCodeGen::generate_ports(Generator* generator) {
    indent_++;
    // sort the names
    const auto& port_names_set = generator->get_port_names();
    std::vector<std::string> port_names(port_names_set.begin(), port_names_set.end());
    std::sort(port_names.begin(), port_names.end());
    // sort again based on the input and output
    // use stable sort to preserve the previous order
    std::stable_sort(port_names.begin(), port_names.end(),
                     [generator](const auto& lhs, const auto& rhs) {
                         auto p_l = generator->get_port(lhs);
                         auto p_r = generator->get_port(rhs);
                         return p_l->port_direction() == PortDirection::In &&
                                p_r->port_direction() == PortDirection::Out;
                     });

    std::unordered_set<std::string> interface_name;

    std::vector<Port*> ports;
    ports.reserve(port_names.size());

    std::vector<std::string> v95_names;
    v95_names.reserve(port_names.size());

    std::vector<std::pair<std::string, std::string>> interface_names;
    interface_names.reserve(port_names.size() / 2);

    for (const auto& port_name : port_names) {
        auto port = generator->get_port(port_name);
        if (!port->is_interface()) {
            ports.emplace_back(port.get());
        } else {
            auto port_interface = port->as<InterfacePort>();
            const auto* ref = port_interface->interface();
            auto const& ref_name = ref->name();
            // only print out interface def once
            if (interface_name.find(ref_name) == interface_name.end()) {
                auto const& def_name = ref->definition()->def_name();
                interface_names.emplace_back(std::make_pair(def_name, ref_name));
                interface_name.emplace(ref_name);
            }
        }
    }

    uint64_t count = 0;
    uint64_t size = interface_names.size() + ports.size();
    for (auto const& [def, ref] : interface_names) {
        count++;
        stream_ << indent() << def << " " << ref;
        if (count != size) stream_ << ",";
        stream_ << stream_.endl();
    }
    for (auto const& port : ports) {
        count++;
        const auto* end = count == size ? "" : ",";
        stream_ << std::make_pair(port, end);
    }
    indent_--;
}

void SystemVerilogCodeGen::generate_variables(Generator* generator) {
    auto const& vars = generator->get_vars();
    for (auto const& var_name : vars) {
        auto const& var = generator->get_var(var_name);
        if (var->type() == VarType::Base && !var->is_interface()) {
            if (options_.yosys_src) output_yosys_src(var.get());
            stream_ << var;
        }
    }
}

void SystemVerilogCodeGen::generate_parameters(Generator* generator) {
    const auto& params = generator->get_params();
    if (!params.empty()) {
        stream_ << "#(" << stream_.endl();
        indent_++;
        uint32_t count = 0;
        for (auto const& [name, param] : params) {
            std::string value_str, type_str;
            if (param->get_initial_value()) {
                auto value = *param->get_initial_value();
                auto c = Const(value, param->width(), param->is_signed());
                value_str = c.to_string();
            } else if (param->param_type() == ParamType::RawType) {
                type_str = "type";
                // determine the initial values
                if (param->get_raw_str_value()) {
                    value_str = *param->get_raw_str_value();
                }
                if (param->get_raw_str_initial_value()) {
                    // use the initial lvalue instead since it's user's intention
                    value_str = *param->get_raw_str_initial_value();
                }
            } else if (param->param_type() == ParamType::Enum) {
                type_str = param->enum_def()->name;
            } else if (param->param_type() != ParamType::Parameter) {
                if (param->has_value()) value_str = param->value_str();
            }
            std::string param_str =
                type_str.empty() ? "parameter" : ::format("parameter {0}", type_str);
            stream_ << indent()
                    << (value_str.empty() ? ::format("{0} {1}", param_str, name)
                                          : ::format("{0} {1} = {2}", param_str, name, value_str));
            if (++count < params.size()) {
                stream_ << ",";
            }
            stream_ << stream_.endl();
        }
        stream_ << ")" << stream_.endl();
        indent_--;
    }
}

void SystemVerilogCodeGen::generate_functions(kratos::Generator* generator) {
    auto funcs = generator->functions();
    for (auto const& iter : funcs) stmt_code(iter.second.get());
}

std::string_view SystemVerilogCodeGen::indent() {
    if (skip_indent_) {
        skip_indent_ = false;
        return "";
    }
    if (empty_indent_str_.size() < (indent_ * indent_size)) {
        // need to expand the string
        std::string result;
        uint32_t num_indent = indent_ * indent_size;
        result.resize(num_indent);
        for (uint32_t i = 0; i < num_indent; i++) result[i] = ' ';
        empty_indent_str_ = result;
        empty_indent_string_view_ = empty_indent_str_;
    }
    return empty_indent_string_view_.substr(0, indent_ * indent_size);
}

std::string_view SystemVerilogCodeGen::pre_indent() {
    if (indent_ == 0) {
        return "";
    } else {
        return empty_indent_string_view_.substr(0, (indent_ - 1) * indent_size);
    }
}

void SystemVerilogCodeGen::dispatch_node(IRNode* node) {
    if (node->ir_node_kind() != IRNodeKind::StmtKind)
        throw StmtException(::format("Cannot codegen non-statement node. Got {0}",
                                     ast_type_to_string(node->ir_node_kind())),
                            {node});
    auto* stmt_ptr = reinterpret_cast<Stmt*>(node);

    // yosys src
    if (options_.yosys_src) output_yosys_src(node);

    // use switch for branch tables
    // also let compiler check if we have all the types covered
    switch (stmt_ptr->type()) {
        case StatementType::Assign:
            stmt_code(reinterpret_cast<AssignStmt*>(node));
            break;
        case StatementType::Block:
            stmt_code(reinterpret_cast<StmtBlock*>(node));
            break;
        case StatementType::If:
            stmt_code(reinterpret_cast<IfStmt*>(node));
            break;
        case StatementType::ModuleInstantiation:
            stmt_code(reinterpret_cast<ModuleInstantiationStmt*>(node));
            break;
        case StatementType::Switch:
            stmt_code(reinterpret_cast<SwitchStmt*>(node));
            break;
        case StatementType::FunctionalCall:
            stmt_code(reinterpret_cast<FunctionCallStmt*>(node));
            break;
        case StatementType::Return:
            stmt_code(reinterpret_cast<ReturnStmt*>(node));
            break;
        case StatementType::Assert:
            stmt_code(reinterpret_cast<AssertBase*>(node));
            break;
        case StatementType::Comment:
            stmt_code(reinterpret_cast<CommentStmt*>(node));
            break;
        case StatementType::InterfaceInstantiation:
            // do nothing
            break;
        case StatementType::RawString:
            stmt_code(reinterpret_cast<RawStringStmt*>(node));
            break;
        case StatementType::For:
            stmt_code(reinterpret_cast<ForStmt*>(node));
            break;
        case StatementType::Auxiliary:
            stmt_code(reinterpret_cast<AuxiliaryStmt*>(node));
            break;
        case StatementType::Break:
            stmt_code(reinterpret_cast<BreakStmt*>(node));
            break;
    }
}

void SystemVerilogCodeGen::stmt_code(AssignStmt* stmt) {
    if (stmt->left()->type() == VarType::PortIO) {
        auto port = stmt->left()->as<Port>();
        if (port->port_direction() == PortDirection::In &&
            stmt->left()->generator() == generator_ &&
            stmt->right()->type() != VarType::ConstValue) {
            throw StmtException("Cannot drive a module's input from itself",
                                {stmt, stmt->left(), stmt->right()});
        }
    }
    stream_ << stmt;
}

void SystemVerilogCodeGen::stmt_code(kratos::ReturnStmt* stmt) {
    if (generator_->debug) stmt->verilog_ln = stream_.line_no();
    stream_ << indent() << "return " << stream_.var_str(stmt->value().get()) << ";"
            << stream_.endl();
}

void SystemVerilogCodeGen::stmt_code(StmtBlock* stmt) {
    switch (stmt->block_type()) {
        case StatementBlockType::Sequential: {
            stmt_code(reinterpret_cast<SequentialStmtBlock*>(stmt));
            break;
        }
        case StatementBlockType::Combinational: {
            stmt_code(reinterpret_cast<CombinationalStmtBlock*>(stmt));
            break;
        }
        case StatementBlockType::Scope: {
            stmt_code(reinterpret_cast<ScopedStmtBlock*>(stmt));
            break;
        }
        case StatementBlockType::Function: {
            stmt_code(reinterpret_cast<FunctionStmtBlock*>(stmt));
            break;
        }
        case StatementBlockType::Initial: {
            stmt_code(reinterpret_cast<InitialStmtBlock*>(stmt));
            break;
        }
        case StatementBlockType::Final: {
            stmt_code(reinterpret_cast<FinalStmtBlock*>(stmt));
            break;
        }
        case StatementBlockType::Latch: {
            stmt_code(reinterpret_cast<LatchStmtBlock*>(stmt));
            break;
        }
    }
}

void SystemVerilogCodeGen::stmt_code(SequentialStmtBlock* stmt) {
    // comment
    if (!stmt->comment.empty()) {
        stream_ << indent() << "// " << strip_newline(stmt->comment) << stream_.endl();
    }
    // produce the sensitive list
    if (generator_->debug) {
        stmt->verilog_ln = stream_.line_no();
    }
    std::vector<std::string> sensitive_list;
    for (const auto& event_control : stmt->get_event_controls()) {
        auto func = [this](const Var* var) { return stream_.var_str(var); };
        sensitive_list.emplace_back(event_control.to_string(func));
    }
    std::string sensitive_list_str =
        string::join(sensitive_list.begin(), sensitive_list.end(), ", ");
    stream_ << stream_.endl() << "always_ff @(" << sensitive_list_str << ") begin"
            << block_label(stmt) << stream_.endl();
    indent_++;

    for (uint64_t i = 0; i < stmt->size(); i++) {
        dispatch_node(stmt->get_child(i));
    }

    indent_--;
    stream_ << indent() << "end" << block_label(stmt) << stream_.endl();
}

void SystemVerilogCodeGen::block_code(const std::string& syntax_name, kratos::StmtBlock* stmt) {
    // comment
    if (!stmt->comment.empty()) {
        stream_ << indent() << "// " << strip_newline(stmt->comment) << stream_.endl();
    }
    if (generator_->debug) {
        stmt->verilog_ln = stream_.line_no();
    }
    stream_ << syntax_name << " begin" << block_label(stmt) << stream_.endl();
    indent_++;

    for (uint64_t i = 0; i < stmt->size(); i++) {
        dispatch_node(stmt->get_child(i));
    }

    indent_--;
    stream_ << indent() << "end" << block_label(stmt) << stream_.endl();
}

void SystemVerilogCodeGen::stmt_code(CombinationalStmtBlock* stmt) {
    std::string keyword = stmt->is_general_purpose() ? "always" : "always_comb";
    block_code(keyword, stmt);
}

void SystemVerilogCodeGen::stmt_code(kratos::InitialStmtBlock* stmt) {
    // comment
    if (!stmt->comment.empty()) {
        stream_ << indent() << "// " << strip_newline(stmt->comment) << stream_.endl();
    }
    if (generator_->debug) {
        stmt->verilog_ln = stream_.line_no();
    }

    stream_ << "initial begin" << block_label(stmt) << stream_.endl();
    indent_++;

    for (uint64_t i = 0; i < stmt->size(); i++) {
        dispatch_node(stmt->get_child(i));
    }

    indent_--;
    stream_ << indent() << "end" << block_label(stmt) << stream_.endl();
}

void SystemVerilogCodeGen::stmt_code(kratos::FinalStmtBlock* stmt) {
    // comment
    if (!stmt->comment.empty()) {
        stream_ << indent() << "// " << strip_newline(stmt->comment) << stream_.endl();
    }
    if (generator_->debug) {
        stmt->verilog_ln = stream_.line_no();
    }

    stream_ << "final begin" << block_label(stmt) << stream_.endl();
    indent_++;

    for (uint64_t i = 0; i < stmt->size(); i++) {
        dispatch_node(stmt->get_child(i));
    }

    indent_--;
    stream_ << indent() << "end" << block_label(stmt) << stream_.endl();
}

void SystemVerilogCodeGen::stmt_code(kratos::ScopedStmtBlock* stmt) {
    if (generator_->debug) {
        stmt->verilog_ln = stream_.line_no();
    }

    stream_ << "begin" << block_label(stmt) << stream_.endl();
    indent_++;

    for (uint64_t i = 0; i < stmt->child_count(); i++) {
        dispatch_node(stmt->get_child(i));
    }

    indent_--;
    stream_ << indent() << "end" << block_label(stmt) << stream_.endl();
}

void SystemVerilogCodeGen::stmt_code(kratos::FunctionStmtBlock* stmt) {
    // dpi is external module
    if (stmt->is_dpi() || stmt->is_builtin()) return;
    if (generator_->debug) {
        stmt->verilog_ln = stream_.line_no();
    }
    if (stmt->is_task()) {
        stream_ << "task ";
    } else {
        std::string return_str;
        if (stmt->has_return_value()) {
            auto handler = stmt->function_handler();
            auto width = 32u;
            if (handler) {
                width = handler->width();
            }
            return_str = "logic" + get_width_str(width) + " ";
        } else {
            return_str = "void ";
        }
        stream_ << "function " << return_str;
    }

    stream_ << stmt->function_name();
    if (stmt->ports().empty()) {
        stream_ << ";" << std::endl;
    } else {
        stream_ << "(" << stream_.endl();
    }

    indent_++;
    uint64_t count = 0;
    auto ports = stmt->ports();
    // if the ordering is specified, use the ordering
    // otherwise use the default map ordering, which is sorted alphabetically
    std::vector<std::string> port_names;
    port_names.reserve(ports.size());
    auto ordering = stmt->port_ordering();
    for (auto const& iter : ports) port_names.emplace_back(iter.first);
    if (!ordering.empty()) {
        if (ordering.size() != ports.size())
            throw InternalException("Port ordering size mismatches ports");
        // sort the list
        std::sort(port_names.begin(), port_names.end(), [&](auto const& lhs, auto const& rhs) {
            return ordering.at(lhs) < ordering.at(rhs);
        });
    }
    for (auto const& port_name : port_names) {
        auto* port = ports.at(port_name).get();
        if (generator_->debug) port->verilog_ln = stream_.line_no();
        stream_ << indent() << get_port_str(port);
        if (++count != ports.size())
            stream_ << "," << stream_.endl();
        else
            stream_ << stream_.endl() << ");" << stream_.endl();
    }
    indent_--;

    stream_ << "begin" << stream_.endl();
    indent_++;
    for (uint64_t i = 0; i < stmt->child_count(); i++) {
        dispatch_node(stmt->get_child(i));
    }
    indent_--;
    auto const* end_token = stmt->is_task() ? "endtask" : "endfunction";
    stream_ << indent() << "end" << stream_.endl() << end_token << stream_.endl();
}

void SystemVerilogCodeGen::stmt_code(AssertBase* stmt) {
    if (stmt->assert_type() == AssertType::AssertValue) {
        auto* st = reinterpret_cast<AssertValueStmt*>(stmt);
        stream_ << indent() << "assert (" << stream_.var_str(st->value()) << ")";
        if (st->else_()) {
            stream_ << " else ";
            // turn off the indent
            auto temp = indent_;
            indent_ = 0;
            dispatch_node(st->else_().get());
            indent_ = temp;
            // dispatch code will close the ;
        } else {
            stream_ << ";" << stream_.endl();
        }
    } else {
        auto st = stmt->as<AssertPropertyStmt>();
        stmt_code(st.get());
    }
}

void SystemVerilogCodeGen::stmt_code(AssertPropertyStmt* stmt) {
    auto* property = stmt->property();
    stream_ << indent() << "property " << property->property_name() << ";" << stream_.endl();
    increase_indent();
    auto edge = property->edge();
    auto* seq = property->sequence();
    if (edge.var) {
        stream_ << indent() << ::format("@({0}) ", edge.to_string([this](const Var* var) {
            return stream_.var_str(var);
        }));
    }
    stream_ << seq->to_string([this](Var* v) { return stream_.var_str(v); }) << ";"
            << stream_.endl();
    decrease_indent();
    stream_ << indent() << "endproperty" << stream_.endl();

    // put assert here
    std::string action;
    auto const action_type = property->action();
    if (action_type == PropertyAction::Assert)
        action = "assert";
    else if (action_type == PropertyAction::Assume)
        action = "assume";
    else if (action_type == PropertyAction::Cover)
        action = "cover";
    else
        return;
    stream_ << indent() << action << " property (" << property->property_name() << ")";
    if (stmt->else_() && action_type == PropertyAction::Assert) {
        dispatch_node(stmt->else_().get());
    } else {
        stream_ << ';' << stream_.endl();
    }
}

void SystemVerilogCodeGen::stmt_code(CommentStmt* stmt) {
    auto const& comments = stmt->comments();
    for (auto const& comment : comments) {
        stream_ << indent() << "// " << comment << stream_.endl();
    }
}

void SystemVerilogCodeGen::stmt_code(RawStringStmt* stmt) {
    auto const& stmts = stmt->stmts();
    for (auto const& line : stmts) {
        // we assume it's already been processed with new lines
        stream_ << indent() << line << stream_.endl();
    }
}

void SystemVerilogCodeGen::stmt_code(IfStmt* stmt) {
    if (generator_->debug) {
        stmt->verilog_ln = stream_.line_no();
        if (stmt->predicate()->verilog_ln == 0) stmt->predicate()->verilog_ln = stream_.line_no();
    }
    stream_ << indent() << "if (" << stream_.var_str(stmt->predicate()) << ") ";
    auto const& then_body = stmt->then_body();
    dispatch_node(then_body.get());

    auto const& else_body = stmt->else_body();
    if (!else_body->empty()) {
        // special case where there is another (and only) if statement nested inside the else body
        // i.e. the else if case
        auto first_stmt = else_body->empty() ? nullptr : else_body->get_stmt(0);
        bool skip = else_body->size() == 1 && (first_stmt->type() == StatementType::Assign ||
                                               first_stmt->type() == StatementType::If ||
                                               first_stmt->type() == StatementType::Return);
        if (skip) {
            stream_ << indent() << "else ";
            skip_indent_ = true;
            else_body->verilog_ln = stream_.line_no();
            dispatch_node((*else_body)[0].get());
        } else {
            stream_ << indent() << "else ";
            dispatch_node(stmt->else_body().get());
        }
    }
}

void SystemVerilogCodeGen::stmt_code(ModuleInstantiationStmt* stmt) {
    // comment
    if (!stmt->comment.empty()) {
        stream_ << indent() << "// " << strip_newline(stmt->comment) << stream_.endl();
    }
    stmt->verilog_ln = stream_.line_no();
    stream_ << indent() << stmt->target()->name;
    const auto& params = stmt->target()->get_params();
    auto debug_info = stmt->port_debug();

    // pre-filter the parameters if the initial value is the same as the current value
    std::unordered_map<std::string, Param*> params_;
    for (auto const& [name, param] : params) {
        if (!param->parent_param() && param->get_initial_value() &&
            (*param->get_initial_value()) == param->value()) {
            continue;
        }
        // could be raw string type as well
        if (param->param_type() == ParamType::RawType &&
            ((param->get_raw_str_value() && param->get_raw_str_initial_value() &&
              (*param->get_raw_str_value()) == (*param->get_raw_str_initial_value())) ||
             (!param->get_raw_str_value() && param->get_raw_str_initial_value()))) {
            continue;
        }
        params_.emplace(std::make_pair(name, param.get()));
    }

    if (!params_.empty()) {
        std::vector<std::string> param_names;
        param_names.reserve(params_.size());
        for (auto const& iter : params_) {
            param_names.emplace_back(iter.first);
        }
        std::sort(param_names.begin(), param_names.end());
        stream_ << " #(" << stream_.endl();
        indent_++;

        uint32_t count = 0;
        for (auto const& name : param_names) {
            auto const& param = params_.at(name);
            auto value = param->value_str();
            if (param->parent_param()) {
                const auto* p = param->parent_param();
                // checking on parameter parent
                auto* p_gen = p->generator();
                if (p_gen != stmt->generator_parent()) {
                    throw VarException(
                        ::format("{0}.{1} is not declared in generator {2}", p_gen->name, p->name,
                                 stmt->generator_parent()->name),
                        {stmt, p_gen, p});
                }
            }
            stream_ << indent()
                    << ::format(
                           ".{0}({1}){2}", name, value,
                           ++count == params_.size() ? ")" : "," + std::string(1, stream_.endl()));
        }

        // start a new line
        stream_ << stream_.endl();
        indent_--;
    } else {
        stream_ << " ";
    }
    stream_ << stmt->target()->instance_name;
    generate_port_interface(stmt);
}

void SystemVerilogCodeGen::stmt_code(kratos::InterfaceInstantiationStmt* stmt) {
    // comment
    if (!stmt->comment.empty()) {
        stream_ << indent() << "// " << strip_newline(stmt->comment) << stream_.endl();
    }
    stmt->verilog_ln = stream_.line_no();
    auto const& interface = stmt->interface();
    stream_ << indent() << interface->definition()->def_name() << " " << interface->name();
    // TODO: allow parametrization
    generate_port_interface(stmt);
}

void SystemVerilogCodeGen::stmt_code(SwitchStmt* stmt) {
    stream_ << indent() << (options_.unique_case ? "unique" : "") << " case ("
            << stream_.var_str(stmt->target()) << ")" << stream_.endl();
    indent_++;
    auto const& body = stmt->body();
    std::vector<std::shared_ptr<Const>> conds;
    conds.reserve(body.size());
    for (auto const& iter : body) {
        if (iter.first) conds.emplace_back(iter.first);
    }
    std::sort(conds.begin(), conds.end(),
              [](const auto& lhs, const auto& rhs) { return lhs->value() < rhs->value(); });
    conds.emplace_back(nullptr);

    for (auto& cond : conds) {
        const auto& stmt_blk = (body.find(cond) != body.end()) ? body.at(cond) : nullptr;
        stream_ << indent() << (cond ? stream_.var_str(cond) : "default") << ": ";
        if (stmt_blk && stmt_blk->empty() && cond) {
            throw VarException(
                ::format("Switch statement condition {0} is empty!", stream_.var_str(cond)),
                {stmt, cond.get()});
        } else if (!stmt_blk || (stmt_blk->empty() && !cond)) {
            //  empty default case
            stream_ << "begin end" << stream_.endl();
        } else {
            // directly output the code if the block only has 1 element
            if (stmt_blk->size() == 1 && label_index_.find(stmt_blk.get()) == label_index_.end() &&
                stmt_blk->get_stmt(0)->type() == StatementType::Assign) {
                skip_indent_ = true;
                dispatch_node((*stmt_blk)[0].get());
            } else {
                indent_++;
                dispatch_node(stmt_blk.get());
                indent_--;
            }
        }
    }

    indent_--;
    stream_ << indent() << "endcase" << stream_.endl();
}

void SystemVerilogCodeGen::stmt_code(kratos::FunctionCallStmt* stmt) {
    // since this is a statement, we don't allow it has return value
    // need to use it as a function call expr instead
    if (stmt->parent()->ir_node_kind() != IRNodeKind::StmtKind) {
        throw StmtException("Function call statement cannot be used in top level", {stmt});
    }
    if (generator_->debug) stmt->verilog_ln = stream_.line_no();
    stream_ << indent() << stream_.var_str(stmt->var());

    stream_ << ";" << stream_.endl();
}

void SystemVerilogCodeGen::stmt_code(kratos::ForStmt* stmt) {
    // for loop
    if (generator_->debug) stmt->verilog_ln = stream_.line_no();
    auto iter = stmt->get_iter_var();

    // get var declaration
    std::vector<std::string> var_decl;
    if (iter->is_gen_var()) {
        // genvar don't have type declaration
        var_decl.emplace_back("genvar");
    } else {
        // maybe add support for much bigger number?
        var_decl.emplace_back("int");
        if (!iter->is_signed()) var_decl.emplace_back("unsigned");
    }

    var_decl.emplace_back(stream_.var_str(iter));
    auto var_decl_str = string::join(var_decl.begin(), var_decl.end(), " ");

    stream_ << indent() << "for (" << var_decl_str << " = ";
    stream_ << ::format("{0}", stmt->start()) << "; " << stream_.var_str(iter)
            << (stmt->end() > stmt->start() ? " < " : " > ");
    stream_ << ::format("{0}", stmt->end()) << "; " << stream_.var_str(iter)
            << (stmt->step() > 0 ? " += " : " -= ");
    stream_ << ::format("{0}", std::abs(stmt->step())) << ") ";
    if (!iter->is_gen_var()) indent_++;
    dispatch_node(stmt->get_loop_body().get());
    if (!iter->is_gen_var()) indent_--;
}

void SystemVerilogCodeGen::stmt_code(LatchStmtBlock* stmt) { block_code("always_latch", stmt); }

void SystemVerilogCodeGen::stmt_code(AuxiliaryStmt* stmt) {
    switch (stmt->aux_type()) {
        case AuxiliaryType::EventTracing: {
            throw UserException("Auxiliary event tracing statement should not be in the codegen!");
        }
        case AuxiliaryType::Delay: {
            stream_ << indent();
            auto const& delay = stmt->as<EventDelayStmt>();
            auto const& event = delay->event();
            auto var_func = [this](const Var* var) { return stream_.var_str(var); };
            switch (event.type) {
                case EventControlType::Delay: {
                    stream_ << event.to_string(var_func);
                    break;
                }
                case EventControlType::Edge: {
                    stream_ << "@(" << event.to_string(var_func) << ')';
                    break;
                }
            }
            stream_ << ';' << stream_.endl();
        }
    }
}

void SystemVerilogCodeGen::stmt_code(BreakStmt*) {
    stream_ << indent() << "break;" << stream_.endl();
}

std::string get_var_size_str(Var* var) {
    std::string str;
    for (uint32_t i = 0; i < var->size().size(); i++) {
        auto* p = var->get_size_param(i);
        if (p)
            str.append(SystemVerilogCodeGen::get_width_str(p));
        else
            str.append(SystemVerilogCodeGen::get_width_str(var->size()[i]));
    }
    return str;
}

std::string SystemVerilogCodeGen::get_port_str(Port* port) {
    std::vector<std::string> strs;
    strs.reserve(8);
    strs.emplace_back(port_dir_to_str(port->port_direction()));
    // we use logic for all inputs and outputs
    if (!port->is_struct() && !port->is_enum() && !port->raw_type_parametrized()) {
        strs.emplace_back("logic");
    } else if (port->is_enum()) {
        auto* enum_def = dynamic_cast<EnumPort*>(port);
        if (!enum_def) throw InternalException("Unable to convert port to enum_def");
        strs.emplace_back(enum_def->enum_type()->name);
    } else if (port->raw_type_parametrized()) {
        auto* p = port->get_raw_type_param();
        strs.emplace_back(p->to_string());
    } else {
        auto* ptr = reinterpret_cast<PortPackedStruct*>(port);
        strs.emplace_back(ptr->packed_struct()->struct_name);
    }
    if (port->is_signed()) strs.emplace_back("signed");
    if ((port->size().front() > 1 || port->size().size() > 1 || port->explicit_array() ||
         port->get_size_param(0)) &&
        port->is_packed()) {
        auto str = get_var_size_str(port);
        strs.emplace_back(str);
    }
    if (!port->is_struct() && !port->is_enum() && !port->raw_type_parametrized()) {
        auto const& var_width_str = get_var_width_str(port);
        if (!var_width_str.empty()) strs.emplace_back(var_width_str);
    }
    strs.emplace_back(port->name);

    if ((port->size().front() > 1 || port->size().size() > 1 || port->explicit_array() ||
         port->get_size_param(0)) &&
        !port->is_packed()) {
        auto str = get_var_size_str(port);
        strs.emplace_back(str);
    }
    return string::join(strs.begin(), strs.end(), " ");
}

std::unordered_map<StmtBlock*, std::string> SystemVerilogCodeGen::index_named_block() {
    std::unordered_map<StmtBlock*, std::string> result;
    auto names = generator_->named_blocks_labels();
    result.reserve(names.size());
    for (auto const& name : names) {
        result.emplace(generator_->get_named_block(name).get(), name);
    }
    return result;
}

std::string SystemVerilogCodeGen::block_label(kratos::StmtBlock* stmt) {
    if (label_index_.find(stmt) != label_index_.end())
        return " :" + label_index_.at(stmt);
    else
        return "";
}

std::string SystemVerilogCodeGen::enum_code(kratos::Enum* enum_) {
    Stream stream_(nullptr, nullptr);
    enum_code_(stream_, enum_, false);
    return stream_.str();
}

void SystemVerilogCodeGen::enum_code_(kratos::Enum* enum_) {
    enum_code_(stream_, enum_, generator_->debug);
}

void SystemVerilogCodeGen::generate_enums(kratos::Generator* generator) {
    auto enums = generator->get_enums();
    for (auto const& iter : enums) enum_code_(iter.second.get());
}

void SystemVerilogCodeGen::generate_port_interface(kratos::InstantiationStmt* stmt) {
    if (stmt->port_mapping().empty()) {
        stream_ << "();" << stream_.endl();
        return;
    }
    stream_ << " (" << stream_.endl();
    indent_++;
    std::vector<std::pair<Port*, Var*>> ports;
    auto const& mapping = stmt->port_mapping();
    ports.reserve(mapping.size());
    for (auto const& iter : mapping) ports.emplace_back(iter);
    std::sort(ports.begin(), ports.end(),
              [](const auto& lhs, const auto& rhs) { return lhs.first->name < rhs.first->name; });
    // sort again based on the input and output
    // use stable sort to preserve the previous order
    std::stable_sort(ports.begin(), ports.end(), [](const auto& lhs, const auto& rhs) {
        return lhs.first->port_direction() == PortDirection::In &&
               rhs.first->port_direction() == PortDirection::Out;
    });

    auto debug_info = stmt->port_debug();
    std::unordered_map<std::string, std::string> interface_names;
    std::vector<std::pair<std::string, std::string>> connections;
    connections.reserve(ports.size());
    for (auto const& [internal, external] : ports) {
        if (generator_->debug && debug_info.find(internal) != debug_info.end()) {
            debug_info.at(internal)->verilog_ln = stream_.line_no();
        }
        std::string internal_name;
        std::string external_name;
        if (stmt->instantiation_type() == InstantiationStmt::InstantiationType::Interface) {
            internal_name = internal->name;
            external_name = external->name;
        } else {
            // module
            if (!internal->is_interface()) {
                internal_name = internal->to_string();
                external_name = external->to_string();
            } else {
                // we assume the interface connectivity has been checked
                // internal has to be an interface
                auto internal_interface = internal->as<InterfacePort>();
                if (!internal_interface) throw InternalException("Unable to cast port");
                const auto* internal_def = internal_interface->interface();
                internal_name = internal_def->name();
                if (internal_def->definition()->is_modport()) {
                    // it's a mod port
                    // get the mod port name
                    auto mod_port_name = internal_def->definition()->name();
                    external_name = external->base_name();
                    // FIXME: this is a little bit hacky here
                    auto potential_name = ::format("{0}.{1}", external_name, mod_port_name);
                    auto i = external->generator()->get_interface(external_name);
                    if (i && !i->definition()->is_modport()) {
                        external_name = potential_name;
                    }
                } else {
                    external_name = external->base_name();
                }

                if (interface_names.find(internal_name) != interface_names.end()) {
                    if (interface_names.at(internal_name) != external_name) {
                        throw StmtException(
                            ::format("{0} and {1} are not from the same interface definition",
                                     internal->handle_name(), external->handle_name()),
                            {internal, external});
                    }
                    continue;
                }
                interface_names.emplace(internal_name, external_name);
            }
        }
        connections.emplace_back(std::make_pair(internal_name, external_name));
    }
    for (uint64_t i = 0; i < connections.size(); i++) {
        auto const& [internal_name, external_name] = connections[i];
        stream_ << indent() << "." << internal_name << "(" << external_name << ")";
        if (i != connections.size() - 1)
            stream_ << "," << stream_.endl();
        else
            stream_ << stream_.endl();
    }
    stream_ << pre_indent() << ");" << stream_.endl() << stream_.endl();
    indent_--;
}

void SystemVerilogCodeGen::generate_interface(Generator* generator) {
    uint64_t stmt_count = generator->stmts_count();
    for (uint64_t i = 0; i < stmt_count; i++) {
        auto stmt = generator->get_stmt(i);
        if (stmt->type() == StatementType::InterfaceInstantiation) {
            auto s = stmt->as<InterfaceInstantiationStmt>();
            stmt_code(s.get());
        }
    }
}

void SystemVerilogCodeGen::enum_code_(kratos::Stream& stream_, kratos::Enum* enum_, bool debug) {
    std::string logic_str = enum_->width() == 1 ? "" : ::format("[{0}:0]", enum_->width() - 1);
    stream_ << "typedef enum logic" << logic_str << " {" << stream_.endl();
    uint32_t count = 0;
    const auto* const indent = "  ";
    // sort it by the values
    std::vector<std::string> names;
    names.reserve(enum_->values.size());
    for (auto const& iter : enum_->values) names.emplace_back(iter.first);
    std::sort(names.begin(), names.end(), [&](const auto& a, const auto& b) {
        return enum_->values.at(a)->value() < enum_->values.at(b)->value();
    });
    for (auto const& name : names) {
        auto& c = enum_->values.at(name);
        if (debug) {
            c->verilog_ln = stream_.line_no();
        }
        stream_ << indent << name << " = " << c->value_string();
        if (++count != enum_->values.size()) stream_ << ",";
        stream_ << stream_.endl();
    }
    stream_ << "} " << enum_->name << ";" << stream_.endl();
}

void SystemVerilogCodeGen::output_yosys_src(IRNode* node) {
    if (!node->fn_name_ln.empty()) {
        auto const& [fn, ln] = node->fn_name_ln[0];
        stream_ << indent() << "(* src = \"" << fn << ":" << ln << "\" *)" << stream_.endl();
    }
}

std::string create_stub(Generator* top) {
    // we can't generate verilog-95 directly from the codegen here here
    auto port_names = top->get_port_names();
    Generator gen(nullptr, top->name);
    for (auto const& port_name : port_names) {
        auto port = top->get_port(port_name);
        auto& p = gen.port(port->port_direction(), port_name, port->var_width(), port->size(),
                           port->port_type(), port->is_signed());
        p.set_is_packed(port->is_packed());
    }
    // that's it
    // now outputting the stream
    auto res = generate_verilog(&gen, {});
    return res.at(top->name);
}

void copy_attrs(const Var& src, Var& target) {
    auto const& attributes = src.get_attributes();
    for (auto const& attr : attributes) {
        target.add_attribute(attr);
    }
}

Generator& create_wrapper_flatten(Generator* top, const std::string& wrapper_name) {
    auto& gen = top->context()->generator(wrapper_name);
    gen.add_child_generator(top->instance_name, top->shared_from_this());
    // copy the parameter definition over
    auto params = top->get_params();
    for (auto const& [name, param] : params) {
        auto& new_p = gen.parameter(name, 32);
        new_p.set_value(param->value());
        param->set_value(new_p.as<Param>());
    }

    auto const& ports = top->get_port_names();
    for (auto const& port_name : ports) {
        auto p = top->get_port(port_name);
        if (p->size().size() == 1 && p->size()[0] == 1) {
            // this is a normal wire
            auto& new_port = gen.port(*p);
            if (p->port_direction() == PortDirection::In) {
                gen.add_stmt(p->assign(new_port, AssignmentType::Blocking));
            } else {
                gen.add_stmt(new_port.assign(p, AssignmentType::Blocking));
            }
            copy_attrs(*p, new_port);
        } else {
            // need to flatten the array
            auto slices = get_flatten_slices(p.get());
            // create port for them based on the slice
            for (auto const& slice : slices) {
                std::string name = port_name;
                for (auto const& s : slice) name = ::format("{0}_{1}", name, s);
                auto* slice_port = &(*p)[slice[0]];
                for (uint64_t i = 1; i < slice.size(); i++) slice_port = &(*slice_port)[slice[i]];
                if (slice_port->size().size() != 1 || slice_port->size()[0] != 1)
                    throw InternalException("Unable to slice ports when flattening");
                auto& new_port = gen.port(p->port_direction(), name, slice_port->var_width());
                if (p->port_direction() == PortDirection::In) {
                    gen.add_stmt(slice_port->assign(new_port, AssignmentType::Blocking));
                } else {
                    gen.add_stmt(
                        new_port.assign(slice_port->shared_from_this(), AssignmentType::Blocking));
                }
                copy_attrs(*p, new_port);
            }
        }
    }
    return gen;
}

std::pair<std::string, uint32_t> generate_sv_package_header(Generator* top,
                                                            const std::string& package_name,
                                                            bool include_guard) {
    Stream stream(nullptr, nullptr);
    // we will write out the dpi and struct ones to the header file
    // this is to ensure everything will be set if this function is called
    // output the guard
    auto struct_info = extract_struct_info(top);
    auto dpi_info = extract_dpi_function(top, true);
    auto enum_info = extract_enum_info(top);
    auto interface_info = extract_interface_info(top);
    if (include_guard) {
        // output the guard
        std::string guard_name = "kratos_" + package_name;
        // make it upper case
        std::for_each(guard_name.begin(), guard_name.end(),
                      [](char& c) { c = static_cast<char>(::toupper(c)); });
        stream << "`ifndef " << guard_name << stream.endl();
        stream << "`define " << guard_name << stream.endl();
        // package header
        stream << "package " << package_name << ";" << stream.endl();
    }

    // all the information list
    auto info_list = {dpi_info, struct_info, enum_info, interface_info};
    for (auto const& info : info_list) {
        for (auto const& iter : info) {
            auto def = iter.second;
            // split on new line to replace with the stream new line so that we can track
            // the new lines
            auto lines = string::get_tokens(def, "\n");
            for (auto const& line : lines) {
                stream << line << stream.endl();
            }
            stream << stream.endl();
        }
    }

    // closing
    stream << "endpackage" << stream.endl();
    // end of guard
    if (include_guard) stream << "`endif" << stream.endl();

    return {stream.str(), static_cast<uint32_t>(stream.line_no())};
}

void fix_verilog_ln(Generator* generator, uint32_t offset) {
    // need to fix every variable and statement verilog line number by an offset
    if (!generator->debug) return;
    // fix the variable declaration
    generator->verilog_ln += offset;
    auto const& var_names = generator->get_all_var_names();
    for (auto const& var_name : var_names) {
        auto var = generator->get_var(var_name);
        var->verilog_ln += offset;
    }
    // get all the statement graph
    StatementGraph graph(generator);
    auto stmts = graph.nodes();
    for (auto const& iter : stmts) {
        auto* stmt = iter.first;
        stmt->verilog_ln += offset;
    }
}

class UniqueGeneratorVisitor : public IRVisitor {
private:
    std::map<std::string, Generator*> generator_map_;

public:
    void visit(Generator* generator) override {
        if (generator_map_.find(generator->name) != generator_map_.end()) {
            return;
        }
        // a unique one
        if (!generator->external()) generator_map_.emplace(generator->name, generator);
    }
    const std::map<std::string, Generator*>& generator_map() const { return generator_map_; };
};

class MarkTrackedVisitor : public IRVisitor {
    void visit(Generator* generator) override {
        auto* context = generator->context();
        if (context) {
            track_lock_.lock();
            context->add_tracked_generator(generator);
            track_lock_.unlock();
        }
    }

    std::mutex track_lock_;
};

void track_generators(Generator* top) {
    // if we need to track if a generator has been touched for verilog
    if (top->context() && top->context()->track_generated()) {
        MarkTrackedVisitor track_visitor;
        track_visitor.visit_generator_root_p(top);
    }
}

std::map<std::string, std::string> generate_verilog_no_pkg(Generator* top,
                                                           SystemVerilogCodeGenOptions options) {
    // this pass assumes that all the generators has been uniquified
    std::map<std::string, std::string> result;
    // first get all the unique generators
    UniqueGeneratorVisitor unique_visitor;
    // this can be parallelized
    unique_visitor.visit_generator_root(top);
    auto const& generator_map = unique_visitor.generator_map();
    // codegen in parallel
    uint32_t num_cpus = get_num_cpus();
    cxxpool::thread_pool pool{num_cpus};
    std::vector<std::future<std::pair<std::string, std::string>>> tasks;
    tasks.reserve(generator_map.size());
    for (const auto& [module_name, module_gen] : generator_map) {
        auto t = pool.push(
            [&options](const std::string& name, Generator* g) {
                SystemVerilogCodeGen codegen(g, options);
                return std::pair(name, codegen.str());
            },
            module_name, module_gen);
        tasks.emplace_back(std::move(t));
    }
    for (auto& t : tasks) {
        auto r = t.get();
        result.emplace(r);
    }

    track_generators(top);
    return result;
}

std::map<uint32_t, std::vector<std::pair<std::string, uint32_t>>> extract_debug_info_gen(
    Generator* top);

void output_pkg_debug_info(const std::map<std::string, Generator*>& generator_map,
                           const SystemVerilogCodeGenOptions& options) {
    for (const auto& [module_name, module_gen] : generator_map) {
        // use unique since we want to keep it close to where it's declared
        auto info = extract_debug_info_gen(module_gen);
        // a simple JSON writer
        std::stringstream json;
        json << "{" << std::endl;
        uint64_t count = 0;
        for (auto const& [line_num, lines] : info) {
            count++;
            json << "  \"" << line_num << "\": [";
            std::vector<std::string> entries;
            entries.reserve(lines.size());
            for (auto const& [f_name, f_ln] : lines) {
                entries.emplace_back(::format("[\"{0}\", {1}]", f_name, f_ln));
            }
            json << string::join(entries.begin(), entries.end(), ", ") << "]";
            if (count != info.size())
                json << "," << std::endl;
            else
                json << std::endl;
        }
        json << "}" << std::endl;
        // just dump it since we don't care about incremental build for debug info
        auto debug_filename = kratos::fs::join(options.output_dir, module_name + ".sv.debug");
        std::ofstream debug_stream(debug_filename, std::ios::in | std::ios::out | std::ios::trunc);
        debug_stream << json.str();
    }
}

void generate_verilog_pkg(Generator* top, SystemVerilogCodeGenOptions options) {
    // input check
    if (options.package_name == top->name) {
        throw UserException(
            ::format("Package name cannot be the same as module name ({0}", top->name));
    }
    // this pass assumes that all the generators has been uniquified
    // first get all the unique generators
    UniqueGeneratorVisitor unique_visitor;
    // this can be parallelized
    unique_visitor.visit_generator_root_p(top);
    auto const& generator_map = unique_visitor.generator_map();
    track_generators(top);

    // we use header_name + ".svh"
    std::string header_filename = options.package_name + ".svh";
    std::map<std::string, std::string> result;
    for (const auto& [module_name, module_gen] : generator_map) {
        SystemVerilogCodeGen codegen(module_gen, options);
        result.emplace(module_name, codegen.str());
    }
    // write out the content to the output_dir
    // we assume output_dir already exists
    // notice that if the content is the same, we don't override to avoid modifying the timestamps
    // this will help with incremental compile in the downstream tools, typically the commercial
    // ones
    // unfortunately verilator doesn't support incremental build. see
    // https://www.veripool.org/boards/2/topics/2822
    for (auto const& [module_name, src] : result) {
        auto path = kratos::fs::join(options.output_dir, module_name + ".sv");
        if (kratos::fs::exists(path)) {
            // load up the file
            std::ifstream in(path);
            std::stringstream content_stream;
            content_stream << in.rdbuf();
            std::string content = content_stream.str();
            if (content == src) continue;
        }
        // truncate mode
        std::ofstream out(path, std::ios::trunc);
        out << src;
        // tell the system where it went, if allowed
        auto gens = top->context()->get_generators_by_name(module_name);
        for (auto const& gen : gens) {
            if (gen->debug) gen->verilog_fn = path;
        }
    }
    // output debug info as well, if required
    if (options.extract_debug_info) {
        output_pkg_debug_info(generator_map, options);
    }

    header_filename = kratos::fs::join(options.output_dir, header_filename);

    // compare it with the old one, if exists. this is for incremental build
    auto values = generate_sv_package_header(top, options.package_name, true);
    auto def_str = values.first;
    if (kratos::fs::exists(header_filename)) {
        std::ifstream in(header_filename);
        std::stringstream content_stream;
        content_stream << in.rdbuf();
        auto content = content_stream.str();
        if (content == def_str) {
            return;
        }
    }
    std::ofstream out(header_filename, std::ios::in | std::ios::out | std::ios::trunc);
    out << def_str;
}

std::map<std::string, std::string> generate_verilog(Generator* top) {
    return generate_verilog(top, {});
}

std::map<std::string, std::string> generate_verilog(Generator* top,
                                                    SystemVerilogCodeGenOptions options) {
    if (options.package_name.empty()) {
        return generate_verilog_no_pkg(top, options);
    } else {
        generate_verilog_pkg(top, options);
        return {};
    }
}

}  // namespace kratos
