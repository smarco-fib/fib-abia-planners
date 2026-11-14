/*********************************************************************
 * abia-planners portability layer: portable random()/srandom().
 *
 * Copyright (C) 2026 Santiago Marco-Sola
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *********************************************************************/

/*
 * An independent implementation of the generator behind glibc's random()
 * with its default state (the "TYPE_3" additive lagged-Fibonacci generator,
 * degree 31, separation 3). It reproduces glibc's output sequence exactly;
 * tests/compat/test_random.c checks this against the C library on glibc.
 *
 * Algorithm (r[] are 32-bit words, arithmetic modulo 2^32):
 *   r[0]  = seed (0 is treated as 1)
 *   r[i]  = 16807 * r[i-1] mod (2^31 - 1)      for i = 1..30
 *   r[i]  = r[i-31]                            for i = 31..33
 *   r[i]  = r[i-31] + r[i-3]                   for i >= 34
 *   the k-th value returned (k = 0, 1, ...) is r[k+344] >> 1.
 * The implementation keeps the last 31 words in a ring buffer.
 *
 * Valid C90 (Metric-FF is compiled with -ansi). Requires 32-bit unsigned int.
 */

#include "compat.h"

#define DEG 31
#define SEP 3

static unsigned int state[DEG];
static int front = SEP;     /* position of r[i-3] */
static int rear = 0;        /* position of r[i-31] */
static int initialised = 0;

/* Compile-time check that unsigned int has 32 bits (C90-compatible trick). */
typedef char compat_assert_uint32[(sizeof(unsigned int) == 4) ? 1 : -1];

static unsigned int next_word( void )
{
  unsigned int value;

  state[front] += state[rear];          /* wraps modulo 2^32 */
  value = state[front];
  if ( ++front >= DEG ) front = 0;
  if ( ++rear >= DEG ) rear = 0;
  return value;
}

void compat_srandom( unsigned int seed )
{
  long word;
  int i;

  if ( seed == 0 ) {
    seed = 1;
  }
  /* glibc keeps the seed in a signed 32-bit word */
  word = (long) (int) seed;
  state[0] = (unsigned int) word;
  for ( i = 1; i < DEG; i++ ) {
    /* 16807 * word mod (2^31 - 1), without overflow (Schrage's method);
     * C90 leaves division of negative numbers implementation-defined, so
     * truncation towards zero is done explicitly. */
    long hi, lo;
    if ( word >= 0 ) {
      hi = word / 127773;
      lo = word % 127773;
    } else {
      hi = -((-word) / 127773);
      lo = -((-word) % 127773);
    }
    word = 16807 * lo - 2836 * hi;
    if ( word < 0 ) {
      word += 2147483647;
    }
    state[i] = (unsigned int) word;
  }
  front = SEP;
  rear = 0;
  initialised = 1;
  /* discard the first 10 * DEG values, as glibc does */
  for ( i = 0; i < 10 * DEG; i++ ) {
    (void) next_word();
  }
}

long compat_random( void )
{
  if ( !initialised ) {
    compat_srandom( 1 );
  }
  return (long) ( next_word() >> 1 );
}
