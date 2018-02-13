#ifndef __ANALYZER_COMMON_H_
#define __ANALYZER_COMMON_H_

#include <stdbool.h>

#define ARGC_MAX 50
#define BUF_SIZE 24000

bool is_same_chr( char* chr1, char *chr2 );

void get_info( char * input, 
               char *org_chr, int *org_pos, 
               char *fnd_chr, int *fnd_pos1, int *fnd_pos2, int *fnd_len, 
               char *base, unsigned int *flag, int *qual, int *ret );

int parse_args( int argc, char *argv[], int *length, int *distance, char *tech );


#endif


