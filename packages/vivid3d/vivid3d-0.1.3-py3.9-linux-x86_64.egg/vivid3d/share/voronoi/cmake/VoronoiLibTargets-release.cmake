#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "voronoi::VoronoiLib" for configuration "Release"
set_property(TARGET voronoi::VoronoiLib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(voronoi::VoronoiLib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libVoronoiLib.so"
  IMPORTED_SONAME_RELEASE "libVoronoiLib.so"
  )

list(APPEND _cmake_import_check_targets voronoi::VoronoiLib )
list(APPEND _cmake_import_check_files_for_voronoi::VoronoiLib "${_IMPORT_PREFIX}/lib/libVoronoiLib.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
