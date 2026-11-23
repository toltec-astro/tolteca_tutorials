# TolTEC C++ Spack system (review deck)

`tula-spack-system.html` is a self-contained HTML deck about the TolTEC C++
build system: TulaCMake, the dependency adapters, the Spack recipes and the
acceptance gates. It moved here from tula_cmake `design/` (last changed in
tula_cmake `646b2d3`, 2026-11-21). The Marp toolchain does not build it;
open the file directly.

The deck predates two changes in tula_cmake `224889f` and `9dae6e2`
(2026-11-22): TulaCMake no longer has a Tlaloc gate, and the acceptance gate
checks required tests instead of test counts. The tula_cmake specification
(`design/spec.md`) owns the current contract.
