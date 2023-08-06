#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "../src/event.hh"
#include "../src/generator.hh"

namespace py = pybind11;

void init_event(py::module &m) {
    using namespace kratos;

    m.def("extract_event_info", &extract_event_info);

    auto event = py::class_<Event>(m, "Event");
    event.def(py::init<std::string>());
    event.def("__call__",
              [](Event &event, const std::map<std::string, std::shared_ptr<Var>> &fields) {
                  return event.fire(fields);
              });
    event.def("__call__", [](Event &event, const py::kwargs &kwargs) {
        std::map<std::string, std::shared_ptr<Var>> fields;
        for (auto const &[name, value] : kwargs) {
            auto var = py::cast<std::shared_ptr<Var>>(value);
            auto name_str = py::cast<std::string>(name);
            fields.emplace(name_str, var);
        }
        return event.fire(fields);
    });

    py::class_<EventInfo>(m, "EventInfo")
        .def_readonly("name", &EventInfo::name)
        .def_readonly("transaction", &EventInfo::transaction)
        .def_readonly("combinational", &EventInfo::combinational)
        .def_readonly("type", &EventInfo::type)
        .def_readonly("fields", &EventInfo::fields)
        .def_readonly("stmt", &EventInfo::stmt)
        .def("__repr__", [](const EventInfo &info) {
            auto dict = py::dict();
            dict["name"] = info.name;
            dict["transaction"] = info.transaction;
            dict["combinational"] = info.combinational;
            dict["type"] = info.type;
            dict["fields"] = info.fields;
            return py::str(dict);
        });

    py::class_<Transaction>(m, "Transaction")
        .def("__repr__", [](const Transaction &t) { return t.name; })
        .def(py::init<std::string>());
}
