# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /root/opencv-2.4.9

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /root/opencv-2.4.9

# Include any dependencies generated for this target.
include modules/core/CMakeFiles/opencv_test_core.dir/depend.make

# Include the progress variables for this target.
include modules/core/CMakeFiles/opencv_test_core.dir/progress.make

# Include the compile flags for this target's objects.
include modules/core/CMakeFiles/opencv_test_core.dir/flags.make

modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o: modules/core/test/test_misc.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_misc.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_misc.cpp > CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_misc.cpp -o CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o: modules/core/test/test_mat.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_mat.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_mat.cpp > CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_mat.cpp -o CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o: modules/core/test/test_ds.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_3)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_ds.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_ds.cpp > CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_ds.cpp -o CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o: modules/core/test/test_math.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_4)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_math.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_math.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_math.cpp > CMakeFiles/opencv_test_core.dir/test/test_math.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_math.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_math.cpp -o CMakeFiles/opencv_test_core.dir/test/test_math.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o: modules/core/test/test_dxt.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_5)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_dxt.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_dxt.cpp > CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_dxt.cpp -o CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o: modules/core/test/test_main.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_6)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_main.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_main.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_main.cpp > CMakeFiles/opencv_test_core.dir/test/test_main.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_main.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_main.cpp -o CMakeFiles/opencv_test_core.dir/test/test_main.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o: modules/core/test/test_eigen.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_7)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_eigen.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_eigen.cpp > CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_eigen.cpp -o CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o: modules/core/test/test_io.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_8)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_io.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_io.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_io.cpp > CMakeFiles/opencv_test_core.dir/test/test_io.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_io.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_io.cpp -o CMakeFiles/opencv_test_core.dir/test/test_io.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o: modules/core/test/test_countnonzero.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_9)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_countnonzero.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_countnonzero.cpp > CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_countnonzero.cpp -o CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o: modules/core/test/test_arithm.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_10)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_arithm.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_arithm.cpp > CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_arithm.cpp -o CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o: modules/core/test/test_rand.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_11)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_rand.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_rand.cpp > CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_rand.cpp -o CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o

modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o: modules/core/CMakeFiles/opencv_test_core.dir/flags.make
modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o: modules/core/test/test_operations.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_12)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -o CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o -c /root/opencv-2.4.9/modules/core/test/test_operations.cpp

modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.i"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -E /root/opencv-2.4.9/modules/core/test/test_operations.cpp > CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.i

modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.s"
	cd /root/opencv-2.4.9/modules/core && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS)  -include "/root/opencv-2.4.9/modules/core/test_precomp.hpp" -Winvalid-pch  -S /root/opencv-2.4.9/modules/core/test/test_operations.cpp -o CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.s

modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o.requires:
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o.requires

modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o.provides: modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o.requires
	$(MAKE) -f modules/core/CMakeFiles/opencv_test_core.dir/build.make modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o.provides.build
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o.provides

modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o.provides.build: modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o

# Object files for target opencv_test_core
opencv_test_core_OBJECTS = \
"CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o" \
"CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o"

# External object files for target opencv_test_core
opencv_test_core_EXTERNAL_OBJECTS =

bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o
bin/opencv_test_core: lib/libopencv_core.so.2.4.9
bin/opencv_test_core: lib/libopencv_ts.a
bin/opencv_test_core: lib/libopencv_highgui.so.2.4.9
bin/opencv_test_core: lib/libopencv_core.so.2.4.9
bin/opencv_test_core: lib/libopencv_flann.so.2.4.9
bin/opencv_test_core: lib/libopencv_imgproc.so.2.4.9
bin/opencv_test_core: lib/libopencv_highgui.so.2.4.9
bin/opencv_test_core: lib/libopencv_features2d.so.2.4.9
bin/opencv_test_core: lib/libopencv_highgui.so.2.4.9
bin/opencv_test_core: lib/libopencv_flann.so.2.4.9
bin/opencv_test_core: lib/libopencv_imgproc.so.2.4.9
bin/opencv_test_core: lib/libopencv_core.so.2.4.9
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/build.make
bin/opencv_test_core: modules/core/CMakeFiles/opencv_test_core.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable ../../bin/opencv_test_core"
	cd /root/opencv-2.4.9/modules/core && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/opencv_test_core.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
modules/core/CMakeFiles/opencv_test_core.dir/build: bin/opencv_test_core
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/build

modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_misc.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_mat.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_ds.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_math.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_dxt.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_main.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_eigen.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_io.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_countnonzero.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_arithm.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_rand.cpp.o.requires
modules/core/CMakeFiles/opencv_test_core.dir/requires: modules/core/CMakeFiles/opencv_test_core.dir/test/test_operations.cpp.o.requires
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/requires

modules/core/CMakeFiles/opencv_test_core.dir/clean:
	cd /root/opencv-2.4.9/modules/core && $(CMAKE_COMMAND) -P CMakeFiles/opencv_test_core.dir/cmake_clean.cmake
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/clean

modules/core/CMakeFiles/opencv_test_core.dir/depend:
	cd /root/opencv-2.4.9 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/opencv-2.4.9 /root/opencv-2.4.9/modules/core /root/opencv-2.4.9 /root/opencv-2.4.9/modules/core /root/opencv-2.4.9/modules/core/CMakeFiles/opencv_test_core.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/core/CMakeFiles/opencv_test_core.dir/depend

