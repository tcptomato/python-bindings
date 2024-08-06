cmake_minimum_required(VERSION 3.16.0)

project(library
    VERSION
        1.0.0
    LANGUAGES
        C
)

set(CMAKE_C_STANDARD 23)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_library(
    ${PROJECT_NAME}
        SHARED
            library.c
)

target_include_directories(
    ${PROJECT_NAME}
        PUBLIC
            $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/>
)

target_link_directories(
    ${PROJECT_NAME}
        PUBLIC
            ${CMAKE_CURRENT_SOURCE_DIR}
)

add_custom_command(
    TARGET
        ${PROJECT_NAME}
    POST_BUILD
    COMMAND
        python3 bindings.py
    VERBATIM
)

add_executable(
${PROJECT_NAME}-app
    main.c
)

target_link_libraries(
    ${PROJECT_NAME}-app
        ${PROJECT_NAME}
)
