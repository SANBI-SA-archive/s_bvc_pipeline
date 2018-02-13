#ifndef _PROB_SHORT_H
#define _PROB_SHORT_H

//#define BUF (1.1)
//#define BUF (1)

//void prob_init_window( int length, float buf_for_pacbio );
//void prob_destroy_window( );

int  prob_long_fill_window( FILE * output, int range, char *chr, int org_pos, int fnd_pos1, int fnd_pos2,
                       char base, int flag, int qual );
int  prob_long_move_window( FILE * output, int range, char *chr, int org_pos, int fnd_pos1, int fnd_pos2, 
                       char base, int flag, int qual );
//void prob_clean_windows( FILE * output, char *org_chr, int org_pos, int length );
//void clean_windows( FILE * output, char *org_chr, int org_pos , int qual, int length );
void prob_long_clean_windows( FILE * output, char * org_chr, int org_pos );

#endif


