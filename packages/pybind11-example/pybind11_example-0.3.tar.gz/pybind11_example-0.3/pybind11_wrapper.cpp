#include <pybind11/pybind11.h>
#include "pybind11_example.h"

namespace py = pybind11;

int chufa(int a, int b)
{
	return a / b;
}


PYBIND11_MODULE(pybind11_example, m) {
	m.doc() = "pybind11 example1 plugin";
	m.def("foo", []() {
		return "Hello world!";
	});
	m.def("chufa", &chufa, "just chufa");
}


