/*
 * Checks compat_random()/compat_srandom() against the C library's
 * random()/srandom(). Only meaningful on glibc (CLAUDE.md rule 10); on other
 * C libraries the reference sequence differs and the test is skipped
 * (exit code 77, the CTest/automake "skipped" convention).
 *
 * Copyright (C) 2026 abia-planners contributors. GPL-2.0-or-later.
 */
#define _DEFAULT_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include "compat.h"

#ifndef __GLIBC__

int main( void )
{
  printf( "SKIP: reference sequence is glibc's; this C library is not glibc\n" );
  return 77;
}

#else

static int compare( const char *label, int n )
{
  int i;
  for ( i = 0; i < n; i++ ) {
    long a = random(), b = compat_random();
    if ( a != b ) {
      printf( "FAIL %s: value %d: libc %ld, compat %ld\n", label, i, a, b );
      return 1;
    }
  }
  return 0;
}

int main( void )
{
  static const unsigned int seeds[] = { 0, 1, 2, 3, 42, 12345, 2147483647u, 2147483648u, 4294967295u };
  unsigned int s;
  size_t i;
  int fails = 0;
  char label[64];

  /* unseeded: both generators start in their default state */
  fails += compare( "unseeded", 10000 );

  for ( i = 0; i < sizeof( seeds ) / sizeof( seeds[0] ); i++ ) {
    srandom( seeds[i] );
    compat_srandom( seeds[i] );
    sprintf( label, "seed %u", seeds[i] );
    fails += compare( label, 10000 );
  }
  /* every seed FF 2.3 can draw from the clock (0..999), shorter runs */
  for ( s = 0; s < 1000; s++ ) {
    srandom( s );
    compat_srandom( s );
    sprintf( label, "seed %u", s );
    fails += compare( label, 1000 );
  }
  /* re-seeding in the middle of a sequence */
  srandom( 7 ); compat_srandom( 7 );
  fails += compare( "seed 7 before re-seed", 500 );
  srandom( 7 ); compat_srandom( 7 );
  fails += compare( "seed 7 after re-seed", 500 );

  if ( fails ) {
    printf( "FAILED: %d sequence(s) differ\n", fails );
    return 1;
  }
  printf( "OK: compat_random() matches glibc random() "
          "(unseeded + 9 seeds x 10000 values, seeds 0..999 x 1000 values, re-seeding)\n" );
  return 0;
}

#endif /* __GLIBC__ */
