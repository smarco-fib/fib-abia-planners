/*********************************************************************
 * abia-planners portability layer, shared by FF 2.3 and Metric-FF 2.1.
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
 * Every platform-specific #ifdef of the project lives in src/compat/.
 * The planners call only the functions declared here (see PATCHES.md, P-COMPAT-*).
 * This header is valid C90, because Metric-FF is compiled with -ansi.
 */

#ifndef ABIA_COMPAT_H
#define ABIA_COMPAT_H

/* ---------------------------------------------------------------------
 * Random numbers: the glibc random()/srandom() sequence on every platform
 * (CLAUDE.md rule 10). Before any call to compat_srandom() the generator is
 * in glibc's default state, i.e. as after srandom(1); srandom(0) behaves
 * like srandom(1), as in glibc.
 */
long compat_random( void );
void compat_srandom( unsigned int seed );

/* ---------------------------------------------------------------------
 * Time.
 *
 * compat_clock_millis(): milliseconds within the current second of the
 * wall clock (0..999). FF 2.3 seeds its generator with this value
 * (upstream: ftime(&tp); srandom(tp.millitm)).
 *
 * compat_times(): CPU time used by the process so far, in hundredths of a
 * second, in the two fields the planners read from POSIX struct tms
 * (their TIME() arithmetic divides by 100). Only the reported times depend
 * on it.
 */
unsigned int compat_clock_millis( void );

struct compat_tms {
  long tms_utime;   /* user CPU time, 1/100 s */
  long tms_stime;   /* system CPU time, 1/100 s */
};
void compat_times( struct compat_tms *t );

#endif /* ABIA_COMPAT_H */
