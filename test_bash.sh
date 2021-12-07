docker run -it --tmpfs /tmp \
    --tmpfs /log \
    --env USERID=$(echo $USERID) \
    --rm --read-only \
    --cap-drop FSETID \
    --cap-drop MKNOD \
    --cap-drop SETFCAP \
    --cap-drop SETPCAP \
    --cap-drop NET_BIND_SERVICE \
    --cap-drop SYS_CHROOT \
    moss_test /bin/bash
