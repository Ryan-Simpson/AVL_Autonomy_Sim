cmake_minimum_required(VERSION 3.8)
project(avl_description)

find_package(ament_cmake REQUIRED)

install(DIRECTORY urdf launch config
  DESTINATION share/${PROJECT_NAME}
)

install(FILES
  ${CMAKE_CURRENT_SOURCE_DIR}/../../gazebo/worlds/igvc_course.sdf
  ${CMAKE_CURRENT_SOURCE_DIR}/../../gazebo/worlds/empty_course.sdf
  DESTINATION share/${PROJECT_NAME}/worlds
)

install(DIRECTORY
  ${CMAKE_CURRENT_SOURCE_DIR}/../../gazebo/models/orange_igvc
  DESTINATION share/${PROJECT_NAME}/models
)

install(PROGRAMS scripts/check_closed_loop.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(closed_loop_contract test/test_closed_loop_contract.py)
endif()

ament_package()
