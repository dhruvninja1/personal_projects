# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Debug")
  file(REMOVE_RECURSE
  "CMakeFiles/ChatClientQt_autogen.dir/AutogenUsed.txt"
  "CMakeFiles/ChatClientQt_autogen.dir/ParseCache.txt"
  "ChatClientQt_autogen"
  )
endif()
