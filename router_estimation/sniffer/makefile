CC = g++
OBJS = interface_capture.o interfaces/interfaces.o interfaces/packet_processing.o
EXEC = wardriving
DEBUG_FLAG = -g
COMP_FLAG = -std=c++11
LIBS_FLAG = -ltins -ljsoncpp -lpcap

$(EXEC) : $(OBJS)
	$(CC) $(DEBUG_FLAG) $(LIBS_FLAG) $(OBJS) -o $@

interfaces/interfaces.o : interfaces/interfaces.cpp interfaces/interfaces.h interfaces/packet_processing.cpp interfaces/packet_processing.h
	$(CC) -c $(DEBUG_FLAG) $(COMP_FLAG) $*.cpp -o $@
interfaces/packet_processing.o : interfaces/packet_processing.cpp interfaces/packet_processing.h
	$(CC) -c $(DEBUG_FLAG) $(COMP_FLAG) $*.cpp -o $@
interface_capture.o : interface_capture.cpp interfaces/interfaces.cpp interfaces/interfaces.h interfaces/packet_processing.cpp interfaces/packet_processing.h
	$(CC) -c $(DEBUG_FLAG) $(COMP_FLAG) $*.cpp
clean:
	rm -f $(OBJS) $(EXEC)
