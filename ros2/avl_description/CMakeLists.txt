cmake_minimum_required(VERSION 3.8)
project(avl_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY urdf launch
  DESTINATION share/${PROJECT_NAME}
)

install(FILES
  ${CMAKE_CURRENT_SOURCE_DIR}/../../gazebo/worlds/empty_course.sdf
  DESTINATION share/${PROJECT_NAME}/worlds
)

ament_package()
