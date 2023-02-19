#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <getopt.h>
#include <assert.h>

#include <sys/socket.h>
#include <sys/ioctl.h>
#include <sys/epoll.h>

#include <netinet/in.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>

int main(int argc, char* const* argv)
{
	int ch;
	int port = 10000;
	size_t content_len = 1, httpdatalen;
	int epfd, sockfd;
	int on;
	char *httpbuf = NULL;
	char *server_ip = NULL;

	while ((ch = getopt(argc, argv, "p:l:a:")) != -1) {
		switch (ch) {
		case 'l':
			content_len = atoi(optarg);
			break;
		case 'a':
			server_ip = optarg;
			break;
		case 'p':
			port = atoi(optarg);
			break;
		default:
			assert(0);
			break;
		}
	}

	printf("listening IP: %s on port: %d\n", server_ip, port);

	{
		size_t buflen = content_len + 256 /* for http hdr */;
		char *content;
		assert((httpbuf = (char *) malloc(buflen)) != NULL);
		assert((content = (char *) malloc(content_len + 1)) != NULL);
		memset(content, 'A', content_len);
		content[content_len] = '\0';
		httpdatalen = snprintf(httpbuf, buflen, "HTTP/1.1 200 OK\r\nContent-Length: %lu\r\nConnection: keep-alive\r\n\r\n%s",
				content_len, content);
		free(content);
		printf("http data length: %lu bytes\n", httpdatalen);
	}

	assert((epfd = epoll_create1(EPOLL_CLOEXEC)) != -1);
	assert((sockfd = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) != -1);
	on = 1;
	assert(!setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on)));
	on = 1;
	assert(!setsockopt(sockfd, SOL_TCP, TCP_NODELAY, &on, sizeof(on)));
	on = 1;
	assert(!ioctl(sockfd, FIONBIO, &on));
	{
		struct sockaddr_in sin = {
			.sin_family = AF_INET,
			.sin_addr.s_addr = inet_addr(server_ip),
			.sin_port = htons(port),
		};
		assert(!bind(sockfd, (struct sockaddr *) &sin, sizeof(sin)));
	}
	assert(!listen(sockfd, SOMAXCONN));
	{
		struct epoll_event ev = {
			.events = EPOLLIN,
			.data.fd = sockfd,
		};
		assert(!epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &ev));
	}

	while (1) {
		struct epoll_event evts[256];
		int i, nfd = epoll_wait(epfd, evts, 256, -1);
		for (i = 0; i < nfd; i++) {
			if (evts[i].data.fd == sockfd) {
				struct sockaddr_in caddr_in;
				socklen_t addrlen;
				int newfd;
				while ((newfd = accept(evts[i].data.fd, (struct sockaddr *)&caddr_in, &addrlen)) != -1) {
					struct epoll_event ev = {
						.events = EPOLLIN,
						.data.fd = newfd,
					};
					assert(!epoll_ctl(epfd, EPOLL_CTL_ADD, newfd, &ev));
				}
			} else {
				ssize_t len;
				static char buf[70000];
				len = read(evts[i].data.fd, buf, sizeof(buf));
				if (len == 0) {
					close(evts[i].data.fd);
					continue;
				} else if (len < 0)
					continue;
				if (strncmp(buf, "GET ", strlen("GET ")) == 0)
					assert(httpdatalen == write(evts[i].data.fd, httpbuf, httpdatalen));
			}
		}
	}

	free(httpbuf);
	
	return 0;
}
