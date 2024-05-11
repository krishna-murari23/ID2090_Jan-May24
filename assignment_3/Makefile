CCOMP = g++ #Initialisng compiler as g++
CFLAGS = -Wall -std=c++11

# Wildcard is used to pass all .cpp files in geomtry to the makefile source
GEO_SRCS = $(wildcard geometry/*.cpp)

# List of corresponding object files for geometry
GEO_OBJS = $(patsubst %.cpp, %.o, $(GEO_SRCS))

# Object file for main.cpp
MAIN_OBJ = main.o

# Target executable is main
EXEC = main

# Compile and line the executables
$(EXEC): $(GEO_OBJS) $(MAIN_OBJ)
	$(CCOMP) $(CFLAGS) $^ -o $@

# Compile .cpp files into .o files
%.o: %.cpp
	$(CCOMP) $(CFLAGS) -c $< -o $@

# Remove executables and object files(make clean)
clean:
	rm $(EXEC) $(GEO_OBJS) $(MAIN_OBJ)
