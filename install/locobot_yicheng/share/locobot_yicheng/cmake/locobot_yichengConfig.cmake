# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_locobot_yicheng_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED locobot_yicheng_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(locobot_yicheng_FOUND FALSE)
  elseif(NOT locobot_yicheng_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(locobot_yicheng_FOUND FALSE)
  endif()
  return()
endif()
set(_locobot_yicheng_CONFIG_INCLUDED TRUE)

# output package information
if(NOT locobot_yicheng_FIND_QUIETLY)
  message(STATUS "Found locobot_yicheng: 0.0.0 (${locobot_yicheng_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'locobot_yicheng' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${locobot_yicheng_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(locobot_yicheng_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${locobot_yicheng_DIR}/${_extra}")
endforeach()
