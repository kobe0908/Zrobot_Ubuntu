aux_source_directory (. SRC)
find_package(OpenCV REQUIRED)
add_library(car_camera_part SHARED ${SRC})
target_link_libraries(car_camera_part ${OpenCV_LIBS})
