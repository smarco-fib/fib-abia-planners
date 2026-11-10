#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdlib.h>
#include <stdio.h>
/* FORCE_SEED=n : srandom(n) at start-up and every srandom() call is replaced by srandom(n)
   RAND15=1     : random() returns only 15 bits (models Windows rand(), RAND_MAX=32767)
   LOG_RANDOM=1 : count random() calls, print to stderr at exit */
static void (*real_srandom)(unsigned);
static long (*real_random)(void);
static long ncalls;
static void report(void){ if(getenv("LOG_RANDOM")) fprintf(stderr,"[shim] random() calls: %ld\n",ncalls); }
__attribute__((constructor)) static void init(void){
  real_srandom=dlsym(RTLD_NEXT,"srandom"); real_random=dlsym(RTLD_NEXT,"random");
  const char*s=getenv("FORCE_SEED"); if(s) real_srandom((unsigned)strtoul(s,0,10));
  atexit(report);
}
void srandom(unsigned seed){ const char*s=getenv("FORCE_SEED"); real_srandom(s?(unsigned)strtoul(s,0,10):seed); }
long random(void){ ncalls++; long r=real_random(); if(getenv("RAND15")) r&=0x7fff; return r; }
