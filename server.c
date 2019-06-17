/* --- Generated the 16/6/2019 at 0:20 --- */
/* --- heptagon compiler, version 1.03.00 (compiled thu. may. 3 2:35:29 CET 2018) --- */
/* --- Command line: /usr/local/bin/heptc -target c -target z3z -s greenhouse greenhouse.ept --- */

#include <netdb.h> 
#include <netinet/in.h> 
#include <stdio.h>
#include <stdlib.h> 
#include <string.h> 
#include <sys/socket.h> 
#include <sys/types.h> 
#include <math.h>
#include "_main.h"

#define MAX 80 
#define PORT 8080 
#define SA struct sockaddr 

Greenhouse__greenhouse_mem mem;

// Function designed for chat between client and server. 
void func(int sockfd) { 
  char buff[MAX];
  int t_in;
  Greenhouse__greenhouse_out _res;
  
  Greenhouse__greenhouse_reset(&mem);
  
  for (;;) { 
    bzero(buff, MAX);
    // read the message from client and copy it in buffer 
    read(sockfd, buff, sizeof(buff)); 
    
    int t_in = round(atof(buff));    
    bzero(buff, MAX);
    Greenhouse__greenhouse_step(t_in, &_res, &mem);
    sprintf(buff, "%d;%d", _res.cooling_on,_res.heater_on);    

    // and send that buffer to client 
    write(sockfd, buff, sizeof(buff));
    printf("%s\n", buff);
    /* fflush(stdout); */

    // if no response then server exit
    // if (sizeof(buff) == 0) break;
  } 
} 

// Driver function 
int main() {
  int sockfd, connfd, len; 
  struct sockaddr_in servaddr, cli; 

  // socket create and verification 
  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd == -1) exit(0);
  
  bzero(&servaddr, sizeof(servaddr)); 

  // assign IP, PORT 
  servaddr.sin_family = AF_INET;
  servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
  servaddr.sin_port = htons(PORT);

  // Binding newly created socket to given IP and verification 
  if ((bind(sockfd, (SA*)&servaddr, sizeof(servaddr))) != 0) exit(0); 
  
  // Now server is ready to listen and verification 
  if ((listen(sockfd, 5)) != 0) exit(0);
  
  len = sizeof(cli); 

  // Accept the data packet from client and verification 
  connfd = accept(sockfd, (SA*)&cli, &len);
  if (connfd < 0) exit(0);
  
  // Function 
  func(connfd);

  // After Function close the socket
  close(sockfd); 
} 
