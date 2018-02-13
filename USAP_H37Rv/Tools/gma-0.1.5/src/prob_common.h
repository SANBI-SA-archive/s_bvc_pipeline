#ifndef _PROB_COMMON_H
#define _PROB_COMMON_H

//#define BUF (1.1)
//#define BUF (1)


#define READ1 0
#define READ2 1

#define FST   0
#define SND   1


typedef struct _prob_elem
{
    // store raw information
    int id;
    char base;
    int  pos;   // org_pos
//    int  length;
    int  flag;
    int  *maq[2];
//    double qual;

    struct _prob_elem * next;

} prob_elem;

typedef struct _prob_window
{
    prob_elem * head;
    prob_elem * tail;
    int size;
    int length;
    int filled;
    int prev_pos;
    int next_pos;

} prob_window;

#ifndef min
    #define min( a, b ) ( ((a) < (b)) ? (a) : (b) ) 
#endif
#ifndef max
    #define max( a, b ) ( ((a) > (b)) ? (a) : (b) ) 
#endif

prob_window pw;


void prob_init_elem( prob_elem * pb, int length );
void prob_init_window( int window_size, int length );
void prob_destroy_window( prob_elem * pb );

//int  prob_fill_window( FILE * output, int range, char *chr, int org_pos, int fnd_pos1, int fnd_pos2,
//                       char base, int flag, int qual, int length );
//int  prob_move_window( FILE * output, int range, char *chr, int org_pos, int fnd_pos1, int fnd_pos2, 
//                       char base, int flag, int qual, int length );
//void prob_clean_windows( FILE * output, char *org_chr, int org_pos );
void prob_print_elem();

#endif


