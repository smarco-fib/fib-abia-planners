# abia-planners: one cross-platform build for FF 2.3 and Metric-FF 2.1.
#
#   cmake -S . -B build/cmake -DCMAKE_BUILD_TYPE=Release
#   cmake --build build/cmake -j 4
#   ctest --test-dir build/cmake
#
# Needs only CMake and a C compiler: the flex/bison output is committed
# (regenerate with tools/regen-parsers.sh; versions in UPSTREAM.md).

cmake_minimum_required(VERSION 3.16)
project(abia_planners VERSION 0.1.0 LANGUAGES C)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

option(ABIA_WERROR "Treat compiler warnings as errors" OFF)
option(ABIA_SANITIZE "Build with AddressSanitizer and UndefinedBehaviorSanitizer" OFF)

# ---------------------------------------------------------------------------
# Flags shared by both planners (see PATCHES.md, P-BUILD-1)
#   -ffp-contract=off  no fused multiply-add: same floating-point results on
#                      every target (no -ffast-math, no -march=native)
if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
  set(ABIA_C_FLAGS -ffp-contract=off -Wall -Wextra)
  if(ABIA_WERROR)
    list(APPEND ABIA_C_FLAGS -Werror)
  endif()
  if(ABIA_SANITIZE)
    list(APPEND ABIA_C_FLAGS -fsanitize=address,undefined -fno-omit-frame-pointer -g)
    add_link_options(-fsanitize=address,undefined)
  endif()
else()
  message(FATAL_ERROR "abia-planners is built with GCC or Clang (MinGW-w64 on Windows); "
                      "${CMAKE_C_COMPILER_ID} is not supported")
endif()

# ---------------------------------------------------------------------------
# Portability layer (C90, like Metric-FF)
add_library(abia_compat STATIC
  src/compat/compat_random.c
  src/compat/compat_time.c)
target_include_directories(abia_compat PUBLIC src/compat)
set_target_properties(abia_compat PROPERTIES C_STANDARD 90 C_EXTENSIONS OFF)
target_compile_options(abia_compat PRIVATE ${ABIA_C_FLAGS})

# ---------------------------------------------------------------------------
# A planner: its sources plus the committed bison output. The bison output
# #includes the flex output (lex.*.c), which is therefore not compiled on its own.
function(abia_planner target dir output_name c_standard c_extensions)
  add_executable(${target} ${ARGN}
    ${dir}/scan-fct_pddl.tab.c
    ${dir}/scan-ops_pddl.tab.c)
  target_include_directories(${target} PRIVATE ${dir})
  target_link_libraries(${target} PRIVATE abia_compat)
  if(NOT WIN32)
    target_link_libraries(${target} PRIVATE m)
  endif()
  target_compile_options(${target} PRIVATE ${ABIA_C_FLAGS})
  set_target_properties(${target} PROPERTIES
    OUTPUT_NAME ${output_name}
    C_STANDARD ${c_standard}
    C_EXTENSIONS ${c_extensions})
endfunction()

# FF 2.3: upstream makefile uses -std=gnu99
set(FF src/ff)
abia_planner(ff ${FF} ff 99 ON
  ${FF}/main.c ${FF}/memory.c ${FF}/output.c ${FF}/parse.c
  ${FF}/inst_pre.c ${FF}/inst_easy.c ${FF}/inst_hard.c ${FF}/inst_final.c
  ${FF}/orderings.c ${FF}/relax.c ${FF}/search.c)

# Metric-FF 2.1: upstream makefile uses -ansi (strict C90)
set(MFF src/metric-ff)
abia_planner(metric_ff ${MFF} metric-ff 90 OFF
  ${MFF}/main.c ${MFF}/memory.c ${MFF}/output.c ${MFF}/parse.c
  ${MFF}/expressions.c ${MFF}/inst_pre.c ${MFF}/inst_easy.c ${MFF}/inst_hard.c
  ${MFF}/inst_final.c ${MFF}/relax.c ${MFF}/search.c)

# ---------------------------------------------------------------------------
# Tests
enable_testing()
add_executable(test_random tests/compat/test_random.c)
target_link_libraries(test_random PRIVATE abia_compat)
set_target_properties(test_random PROPERTIES C_STANDARD 99 C_EXTENSIONS ON)
add_test(NAME compat_random_matches_glibc COMMAND test_random)
set_tests_properties(compat_random_matches_glibc PROPERTIES SKIP_RETURN_CODE 77)
