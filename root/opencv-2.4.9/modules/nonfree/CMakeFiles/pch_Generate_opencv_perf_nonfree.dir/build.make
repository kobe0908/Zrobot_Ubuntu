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

# Utility rule file for pch_Generate_opencv_perf_nonfree.

# Include the progress variables for this target.
include modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree.dir/progress.make

modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree: modules/nonfree/perf_precomp.hpp.gch/opencv_perf_nonfree_RELEASE.gch

modules/nonfree/perf_precomp.hpp.gch/opencv_perf_nonfree_RELEASE.gch: modules/nonfree/perf/perf_precomp.hpp
modules/nonfree/perf_precomp.hpp.gch/opencv_perf_nonfree_RELEASE.gch: modules/nonfree/perf_precomp.hpp
modules/nonfree/perf_precomp.hpp.gch/opencv_perf_nonfree_RELEASE.gch: lib/libopencv_perf_nonfree_pch_dephelp.a
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating perf_precomp.hpp.gch/opencv_perf_nonfree_RELEASE.gch"
	cd /root/opencv-2.4.9/modules/nonfree && /usr/bin/cmake -E make_directory /root/opencv-2.4.9/modules/nonfree/perf_precomp.hpp.gch
	cd /root/opencv-2.4.9/modules/nonfree && /usr/bin/c++ -O3 -DNDEBUG -DNDEBUG -I"/root/opencv-2.4.9/modules/nonfree/perf" -I"/root/opencv-2.4.9/modules/features2d/include" -I"/root/opencv-2.4.9/modules/highgui/include" -I"/root/opencv-2.4.9/modules/imgproc/include" -I"/root/opencv-2.4.9/modules/flann/include" -I"/root/opencv-2.4.9/modules/core/include" -I"/root/opencv-2.4.9/modules/ts/include" -I"/root/opencv-2.4.9/modules/nonfree/include" -I"/root/opencv-2.4.9/modules/ocl/include" -I"/root/opencv-2.4.9/modules/gpu/include" -I"/root/opencv-2.4.9/modules/photo/include" -I"/root/opencv-2.4.9/modules/objdetect/include" -I"/root/opencv-2.4.9/modules/legacy/include" -I"/root/opencv-2.4.9/modules/video/include" -I"/root/opencv-2.4.9/modules/ml/include" -I"/root/opencv-2.4.9/modules/calib3d/include" -I"/root/opencv-2.4.9/modules/nonfree" -I"/root/opencv-2.4.9/modules/nonfree/src" -I"/root/opencv-2.4.9/modules/nonfree/test" -isystem"/root/opencv-2.4.9/3rdparty/include/opencl/1.2" -isystem"/root/opencv-2.4.9" -fsigned-char -W -Wall -Werror=return-type -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Winit-self -Wpointer-arith -Wsign-promo -fdiagnostics-show-option -pthread -fomit-frame-pointer -ffunction-sections -Wno-undef -Wno-shadow -x c++-header -o /root/opencv-2.4.9/modules/nonfree/perf_precomp.hpp.gch/opencv_perf_nonfree_RELEASE.gch /root/opencv-2.4.9/modules/nonfree/perf_precomp.hpp

modules/nonfree/perf_precomp.hpp: modules/nonfree/perf/perf_precomp.hpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating perf_precomp.hpp"
	cd /root/opencv-2.4.9/modules/nonfree && /usr/bin/cmake -E copy /root/opencv-2.4.9/modules/nonfree/perf/perf_precomp.hpp /root/opencv-2.4.9/modules/nonfree/perf_precomp.hpp

pch_Generate_opencv_perf_nonfree: modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree
pch_Generate_opencv_perf_nonfree: modules/nonfree/perf_precomp.hpp.gch/opencv_perf_nonfree_RELEASE.gch
pch_Generate_opencv_perf_nonfree: modules/nonfree/perf_precomp.hpp
pch_Generate_opencv_perf_nonfree: modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree.dir/build.make
.PHONY : pch_Generate_opencv_perf_nonfree

# Rule to build all files generated by this target.
modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree.dir/build: pch_Generate_opencv_perf_nonfree
.PHONY : modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree.dir/build

modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree.dir/clean:
	cd /root/opencv-2.4.9/modules/nonfree && $(CMAKE_COMMAND) -P CMakeFiles/pch_Generate_opencv_perf_nonfree.dir/cmake_clean.cmake
.PHONY : modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree.dir/clean

modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree.dir/depend:
	cd /root/opencv-2.4.9 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/opencv-2.4.9 /root/opencv-2.4.9/modules/nonfree /root/opencv-2.4.9 /root/opencv-2.4.9/modules/nonfree /root/opencv-2.4.9/modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/nonfree/CMakeFiles/pch_Generate_opencv_perf_nonfree.dir/depend

