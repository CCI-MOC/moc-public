FILEDIR=mocpoc/files/headnode
GETFILES=\
	$(FILEDIR)/vmlinuz\
	$(FILEDIR)/initrd.img
MIRROR=http://mirror.mit.edu/centos/6.4/os/x86_64

all: $(GETFILES)
clean:
	rm -f $(GETFILES)

$(GETFILES):
	cd $(FILEDIR); wget $(MIRROR)/isolinux/`basename $@`
