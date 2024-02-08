#include "redtime.h"
#include "pybind11/pybind11.h"

namespace py = pybind11;

use namespace redtime;

PYBIND11_MODULE(redtime, m) {
	py::class_<freetime>(m, "freetime")
		.def(py::init)
}