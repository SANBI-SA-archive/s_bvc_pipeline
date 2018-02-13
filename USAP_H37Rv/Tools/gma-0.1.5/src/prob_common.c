#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

#include "prob_common.h"
#include "resource.h"


void prob_init_elem( prob_elem * pb, int size )
{
    if( pb->pos > 0 )
    {
        if( ( pb->maq[READ1] == NULL ) || ( pb->maq[READ2] == NULL ) ) 
        {
            fprintf( stderr, "%s already used, but null mem location for maq\n", ERR_009 );
        }
    }
    else 
    {
        pb->maq[READ1] = malloc( sizeof(int) * size );      // for buffer
        //memset( pb->maq[READ1], 0, sizeof(int) * length );
    
        pb->maq[READ2] = malloc( sizeof(int) * size );      // for buffer
        //memset( pb->maq[READ2], 0, sizeof(int) * length );
    
        //fprintf( stderr, "%s prob_init_elem called\n", INFO_008 );
    
    }
    memset( pb->maq[READ1], 0, sizeof(int) * size );
    memset( pb->maq[READ2], 0, sizeof(int) * size );

    pb->base = '*';
    pb->pos = 0;
    //pb->length = length;
    pb->flag = -1;
}



//void prob_print_elem( int length )
void prob_print_elem( )
{
    int i = 0;
    prob_elem * pb = pw.head;

    while( pb != NULL )
    { 
        fprintf( stderr, "%d(%p:%d-%d)\t(", pb->id, pb, pb->pos, pb->pos + pw.size - 1 );

        for( i = 0; i < pw.size ; i++ )
        {
            fprintf( stderr, "%2d ", pb->maq[READ1][i]);
        }
        fprintf( stderr, ")\n");
        pb = pb->next;
     }
}


void prob_init_window( int window_size, int length )
{
    int i = 0;
    int id = 1;
    prob_elem * tmp;

    //pw.cov = 0;
    pw.prev_pos = 0; // the position that we expect
    pw.size = window_size;
    pw.length = length;
    pw.filled = 0;
 
    pw.head = malloc( sizeof( prob_elem ) );
    memset( pw.head, 0, sizeof( prob_elem ) );

    prob_init_elem( pw.head, length );
    pw.head->id = id++;
    fprintf( stderr, "%s head id : %p(%d), size: %d\n", INFO_009, pw.head, pw.head->id, pw.size );
 
    tmp = pw.head;
    
    for( i = 0; i < (pw.size- 1); i++ )  // to make coverage 100x + buffer
    {
        tmp->next = malloc( sizeof( prob_elem ) );
        memset( tmp->next, 0, sizeof( prob_elem ) );

        tmp = tmp->next;
        tmp->id = i+2;

        tmp->next = NULL;

        prob_init_elem( tmp, length );
        fprintf( stderr, "%s tmp: %p(%d)\n", INFO_010, tmp, tmp->id );
    }    

    pw.tail = pw.head;

   // prob_print_elem(length);

//fprintf( stderr, "length : %d\n", length );

//    printf("[head] %p\n", pw.head );
//    printf("[tail] %p\n", pw.tail );

//    tmp = pw.head;

//    for( i = 0; i < length; i++ )
//    {
//        printf("[%d] %p->%p\n", i, tmp, tmp->next );
//        tmp = tmp->next;
//    }

}


void prob_destroy_window( prob_elem * head )
{
    int i = 0;
    prob_elem * pb = NULL;
    prob_elem * tmp = NULL;

    if( head == NULL )
    {
        pb = pw.head;
    }
    else
    {
        pb = head;
    } 

    tmp = pb->next;

    fprintf( stderr, "%s pw.size(%d)\n", INFO_025, pw.size );

    for( i = 0; i < pw.size; i++ )
    {
        //fprintf( stderr, "%s i(%d) free(%p) id(%d) pb->next(%p) ", INFO_026, i, pb, pb->id, pb->next );
        free( pb );
        pb = tmp;
        if( tmp != NULL )
        {   tmp = tmp->next;
        }
    }
   
    //pw.cov = 0;
    pw.head = NULL;
    pw.tail = NULL; 
}

/*
void cleanup_window_list( prob_elem * hd, int read, char *chr, int pos1, int pos2 )
{
    int i = 0, j = 0;
    int qual = 0;
    int cvg = 0;

    double p_err = 0.0;
    double p_acc = 0.0;
    double gms = 0.0;

    prob_elem * elem = pw.head;
    prob_elem * head = pw.head;

    fprintf( stderr, "%s pos1:%d, pos2(%d)\n", INFO_028, pos1, pos2 );
    //prob_print_elem();
    
    for( i = pos1; i < pos2; i++ )
    {
    
        elem = head;
        fprintf( stderr, "%s i(%d), elem->pos(%d), pw.filled(%d), pw.tail->pos(%d)\n", INFO_029, i, elem->pos, pw.filled, pw.tail->pos  );

        for( j = 0; j < (pw.filled) ; j++ )
        {
            qual = elem->maq[read][i- elem->pos];         
            p_err = pow( (double)0.1, (qual/10.0) );
            p_acc += (1 - p_err);
            if( qual > 0 )
            {
                cvg++;
            }
            fprintf( stderr, "%s j:%d, elem->id(%d) elem->next(%p) qual(%d) cvg(%d) \n", INFO_011, j, elem->id, elem->next, qual, cvg );
    
            elem = elem->next;
        }
    
        if( pw.filled <= 0 )
        {
            gms = 0.0;
            pw.filled = 0;
        }
        else
        {
            gms = (p_acc / pw.filled) * 100;
        }
     
        if(  pw.tail->pos == i )
        { 

            fprintf( stderr, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i, pw.tail->base, cvg, gms );
            fprintf( stdout, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i, pw.tail->base, cvg, gms );
        }
        else
        { 
            fprintf( stderr, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i, '*', cvg, gms );
            fprintf( stdout, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i, '*', cvg, gms );
        }
    
        //elem = pw.heada
        head = head->next;
        pw.filled--;
        p_acc = 0.0;
        p_err = 0.0;
        gms = 0.0;
        cvg = 0;
       
    }
}



void prob_clean_windows( FILE * output, char * org_chr, int org_pos )
{
    cleanup_window_list( pw.head, READ1, org_chr, org_pos, ( org_pos + pw.size ) );
}

*/
