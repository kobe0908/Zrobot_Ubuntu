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
include modules/python/CMakeFiles/opencv_python.dir/depend.make

# Include the progress variables for this target.
include modules/python/CMakeFiles/opencv_python.dir/progress.make

# Include the compile flags for this target's objects.
include modules/python/CMakeFiles/opencv_python.dir/flags.make

modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o: modules/python/CMakeFiles/opencv_python.dir/flags.make
modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o: modules/python/src2/cv2.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o"
	cd /root/opencv-2.4.9/modules/python && /usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/opencv_python.dir/src2/cv2.cpp.o -c /root/opencv-2.4.9/modules/python/src2/cv2.cpp

modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_python.dir/src2/cv2.cpp.i"
	cd /root/opencv-2.4.9/modules/python && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /root/opencv-2.4.9/modules/python/src2/cv2.cpp > CMakeFiles/opencv_python.dir/src2/cv2.cpp.i

modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_python.dir/src2/cv2.cpp.s"
	cd /root/opencv-2.4.9/modules/python && /usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /root/opencv-2.4.9/modules/python/src2/cv2.cpp -o CMakeFiles/opencv_python.dir/src2/cv2.cpp.s

modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o.requires:
.PHONY : modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o.requires

modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o.provides: modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o.requires
	$(MAKE) -f modules/python/CMakeFiles/opencv_python.dir/build.make modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o.provides.build
.PHONY : modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o.provides

modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o.provides.build: modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o

modules/python/generated0.i: modules/python/src2/api
modules/python/generated0.i: modules/python/src2/defs
modules/python/generated0.i: modules/python/src2/gen.py
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_2)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating generated0.i"
	cd /root/opencv-2.4.9/modules/python && /usr/bin/python /root/opencv-2.4.9/modules/python/src2/gen.py /root/opencv-2.4.9/modules/python/src2

modules/python/pyopencv_generated_funcs.h: modules/python/src2/gen2.py
modules/python/pyopencv_generated_funcs.h: modules/python/src2/hdr_parser.py
modules/python/pyopencv_generated_funcs.h: modules/core/include/opencv2/core/core.hpp
modules/python/pyopencv_generated_funcs.h: modules/flann/include/opencv2/flann/miniflann.hpp
modules/python/pyopencv_generated_funcs.h: modules/imgproc/include/opencv2/imgproc/imgproc.hpp
modules/python/pyopencv_generated_funcs.h: modules/video/include/opencv2/video/background_segm.hpp
modules/python/pyopencv_generated_funcs.h: modules/video/include/opencv2/video/tracking.hpp
modules/python/pyopencv_generated_funcs.h: modules/photo/include/opencv2/photo/photo.hpp
modules/python/pyopencv_generated_funcs.h: modules/highgui/include/opencv2/highgui/highgui.hpp
modules/python/pyopencv_generated_funcs.h: modules/ml/include/opencv2/ml/ml.hpp
modules/python/pyopencv_generated_funcs.h: modules/features2d/include/opencv2/features2d/features2d.hpp
modules/python/pyopencv_generated_funcs.h: modules/calib3d/include/opencv2/calib3d/calib3d.hpp
modules/python/pyopencv_generated_funcs.h: modules/objdetect/include/opencv2/objdetect/objdetect.hpp
modules/python/pyopencv_generated_funcs.h: modules/contrib/include/opencv2/contrib/contrib.hpp
modules/python/pyopencv_generated_funcs.h: modules/nonfree/include/opencv2/nonfree/features2d.hpp
modules/python/pyopencv_generated_funcs.h: modules/nonfree/include/opencv2/nonfree/nonfree.hpp
	$(CMAKE_COMMAND) -E cmake_progress_report /root/opencv-2.4.9/CMakeFiles $(CMAKE_PROGRESS_3)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Generating pyopencv_generated_funcs.h, pyopencv_generated_func_tab.h, pyopencv_generated_types.h, pyopencv_generated_type_reg.h, pyopencv_generated_const_reg.h"
	cd /root/opencv-2.4.9/modules/python && /usr/bin/python /root/opencv-2.4.9/modules/python/src2/gen2.py /root/opencv-2.4.9/modules/python /root/opencv-2.4.9/modules/core/include/opencv2/core/core.hpp /root/opencv-2.4.9/modules/flann/include/opencv2/flann/miniflann.hpp /root/opencv-2.4.9/modules/imgproc/include/opencv2/imgproc/imgproc.hpp /root/opencv-2.4.9/modules/video/include/opencv2/video/background_segm.hpp /root/opencv-2.4.9/modules/video/include/opencv2/video/tracking.hpp /root/opencv-2.4.9/modules/photo/include/opencv2/photo/photo.hpp /root/opencv-2.4.9/modules/highgui/include/opencv2/highgui/highgui.hpp /root/opencv-2.4.9/modules/ml/include/opencv2/ml/ml.hpp /root/opencv-2.4.9/modules/features2d/include/opencv2/features2d/features2d.hpp /root/opencv-2.4.9/modules/calib3d/include/opencv2/calib3d/calib3d.hpp /root/opencv-2.4.9/modules/objdetect/include/opencv2/objdetect/objdetect.hpp /root/opencv-2.4.9/modules/contrib/include/opencv2/contrib/contrib.hpp /root/opencv-2.4.9/modules/nonfree/include/opencv2/nonfree/features2d.hpp /root/opencv-2.4.9/modules/nonfree/include/opencv2/nonfree/nonfree.hpp

modules/python/pyopencv_generated_func_tab.h: modules/python/pyopencv_generated_funcs.h

modules/python/pyopencv_generated_types.h: modules/python/pyopencv_generated_funcs.h

modules/python/pyopencv_generated_type_reg.h: modules/python/pyopencv_generated_funcs.h

modules/python/pyopencv_generated_const_reg.h: modules/python/pyopencv_generated_funcs.h

# Object files for target opencv_python
opencv_python_OBJECTS = \
"CMakeFiles/opencv_python.dir/src2/cv2.cpp.o"

# External object files for target opencv_python
opencv_python_EXTERNAL_OBJECTS =

lib/cv2.so: modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o
lib/cv2.so: /usr/lib/libpython2.7.so
lib/cv2.so: lib/libopencv_core.so.2.4.9
lib/cv2.so: lib/libopencv_flann.so.2.4.9
lib/cv2.so: lib/libopencv_imgproc.so.2.4.9
lib/cv2.so: lib/libopencv_highgui.so.2.4.9
lib/cv2.so: lib/libopencv_features2d.so.2.4.9
lib/cv2.so: lib/libopencv_calib3d.so.2.4.9
lib/cv2.so: lib/libopencv_ml.so.2.4.9
lib/cv2.so: lib/libopencv_video.so.2.4.9
lib/cv2.so: lib/libopencv_legacy.so.2.4.9
lib/cv2.so: lib/libopencv_objdetect.so.2.4.9
lib/cv2.so: lib/libopencv_photo.so.2.4.9
lib/cv2.so: lib/libopencv_gpu.so.2.4.9
lib/cv2.so: lib/libopencv_ocl.so.2.4.9
lib/cv2.so: lib/libopencv_nonfree.so.2.4.9
lib/cv2.so: lib/libopencv_contrib.so.2.4.9
lib/cv2.so: lib/libopencv_nonfree.so.2.4.9
lib/cv2.so: lib/libopencv_gpu.so.2.4.9
lib/cv2.so: lib/libopencv_legacy.so.2.4.9
lib/cv2.so: lib/libopencv_photo.so.2.4.9
lib/cv2.so: lib/libopencv_ocl.so.2.4.9
lib/cv2.so: lib/libopencv_calib3d.so.2.4.9
lib/cv2.so: lib/libopencv_features2d.so.2.4.9
lib/cv2.so: lib/libopencv_flann.so.2.4.9
lib/cv2.so: lib/libopencv_ml.so.2.4.9
lib/cv2.so: lib/libopencv_video.so.2.4.9
lib/cv2.so: lib/libopencv_objdetect.so.2.4.9
lib/cv2.so: lib/libopencv_highgui.so.2.4.9
lib/cv2.so: lib/libopencv_imgproc.so.2.4.9
lib/cv2.so: lib/libopencv_core.so.2.4.9
lib/cv2.so: modules/python/CMakeFiles/opencv_python.dir/build.make
lib/cv2.so: modules/python/CMakeFiles/opencv_python.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX shared library ../../lib/cv2.so"
	cd /root/opencv-2.4.9/modules/python && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/opencv_python.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
modules/python/CMakeFiles/opencv_python.dir/build: lib/cv2.so
.PHONY : modules/python/CMakeFiles/opencv_python.dir/build

modules/python/CMakeFiles/opencv_python.dir/requires: modules/python/CMakeFiles/opencv_python.dir/src2/cv2.cpp.o.requires
.PHONY : modules/python/CMakeFiles/opencv_python.dir/requires

modules/python/CMakeFiles/opencv_python.dir/clean:
	cd /root/opencv-2.4.9/modules/python && $(CMAKE_COMMAND) -P CMakeFiles/opencv_python.dir/cmake_clean.cmake
.PHONY : modules/python/CMakeFiles/opencv_python.dir/clean

modules/python/CMakeFiles/opencv_python.dir/depend: modules/python/generated0.i
modules/python/CMakeFiles/opencv_python.dir/depend: modules/python/pyopencv_generated_funcs.h
modules/python/CMakeFiles/opencv_python.dir/depend: modules/python/pyopencv_generated_func_tab.h
modules/python/CMakeFiles/opencv_python.dir/depend: modules/python/pyopencv_generated_types.h
modules/python/CMakeFiles/opencv_python.dir/depend: modules/python/pyopencv_generated_type_reg.h
modules/python/CMakeFiles/opencv_python.dir/depend: modules/python/pyopencv_generated_const_reg.h
	cd /root/opencv-2.4.9 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /root/opencv-2.4.9 /root/opencv-2.4.9/modules/python /root/opencv-2.4.9 /root/opencv-2.4.9/modules/python /root/opencv-2.4.9/modules/python/CMakeFiles/opencv_python.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/python/CMakeFiles/opencv_python.dir/depend

