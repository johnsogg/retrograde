# Points to the root of Google Test
GTEST_DIR = /Users/johnsogg/Projects/retrograde/gtest-1.6.0

GTEST_LIB = $(GTEST_DIR)/make/gtest_main.a

# All tests produced by this Makefile.  ADD TO THIS LIST.
TESTS = linked_list_test

# Where to find user code.
USER_DIR = .

# Flags passed to the preprocessor.
CPPFLAGS += -I$(GTEST_DIR)/include

# Flags passed to the C++ compiler.
CXXFLAGS += -g -Wall -Wextra

# All Google Test headers.  Usually you shouldn't change this
# definition.
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h \
                $(GTEST_DIR)/include/gtest/internal/*.h

# House-keeping build targets.

all : $(TESTS)

clean :
	rm -f $(TESTS) *.o

RetroPrinter.o : $(USER_DIR)/RetroPrinter.cpp \
                 $(GTEST_HEADERS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/RetroPrinter.cpp

# Assignment-specific build rules below.

linked_list.o : $(USER_DIR)/linked_list.cpp \
                $(USER_DIR)/linked_list.h \
                $(GTEST_HEADERS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/linked_list.cpp

linked_list_test.o : $(USER_DIR)/linked_list_test.cpp \
                     $(USER_DIR)/linked_list.h \
                     $(GTEST_HEADERS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/linked_list_test.cpp

linked_list_test : linked_list.o \
                   linked_list_test.o \
                   RetroPrinter.o \
		   $(GTEST_LIB)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -lpthread $^ -o $@


