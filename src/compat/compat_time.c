/*********************************************************************
 * abia-planners portability layer: wall-clock milliseconds and CPU time.
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

#if !defined(_WIN32) && !defined(_POSIX_C_SOURCE)
#define _POSIX_C_SOURCE 200112L   /* gettimeofday, getrusage under -ansi */
#endif

#include "compat.h"

#ifdef _WIN32

#define WIN32_LEAN_AND_MEAN
#include <windows.h>

unsigned int compat_clock_millis( void )
{
  SYSTEMTIME st;
  GetSystemTime( &st );
  return (unsigned int) st.wMilliseconds;
}

/* FILETIME counts 100-nanosecond intervals; 1/100 s = 100000 of them. */
static long filetime_to_centiseconds( const FILETIME *ft )
{
  ULARGE_INTEGER u;
  u.LowPart = ft->dwLowDateTime;
  u.HighPart = ft->dwHighDateTime;
  return (long) ( u.QuadPart / 100000 );
}

void compat_times( struct compat_tms *t )
{
  FILETIME creation, exit_time, kernel, user;
  if ( GetProcessTimes( GetCurrentProcess(), &creation, &exit_time, &kernel, &user ) ) {
    t->tms_utime = filetime_to_centiseconds( &user );
    t->tms_stime = filetime_to_centiseconds( &kernel );
  } else {
    t->tms_utime = 0;
    t->tms_stime = 0;
  }
}

#else /* POSIX */

#include <stddef.h>
#include <sys/time.h>
#include <sys/resource.h>

unsigned int compat_clock_millis( void )
{
  struct timeval tv;
  gettimeofday( &tv, NULL );
  return (unsigned int) ( tv.tv_usec / 1000 );
}

void compat_times( struct compat_tms *t )
{
  struct rusage ru;
  if ( getrusage( RUSAGE_SELF, &ru ) == 0 ) {
    t->tms_utime = (long) ru.ru_utime.tv_sec * 100 + (long) ru.ru_utime.tv_usec / 10000;
    t->tms_stime = (long) ru.ru_stime.tv_sec * 100 + (long) ru.ru_stime.tv_usec / 10000;
  } else {
    t->tms_utime = 0;
    t->tms_stime = 0;
  }
}

#endif
