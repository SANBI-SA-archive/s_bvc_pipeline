#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdbool.h>

#include "prob_common.h"
#include "prob_long.h"
#include "resource.h"


static void circulate_window_list( prob_elem * hd, int read, char *chr, int fnd_pos1, int fnd_pos2 )
{
    int i = 0, j = 0; 
    int qual = 0;
    int cvg = 0;
    double p_err = 0.0;
    double p_acc = 0.0;
    double gms = 0.0;
    prob_elem * elem = pw.head;
    int offset = 0;

    for( i = fnd_pos1-1; i < fnd_pos2-1; i++ )
    {
        elem = pw.head;
        p_acc = 0.0;
        p_err = 0.0;
        gms = 0.0;
        cvg = 0;

//        fprintf( stderr, "%sL pw.head->id(%d), pw.tail->id(%d) i(%d), (%d-%d)\n", INFO_013, pw.head->id, pw.tail->id, i, fnd_pos1, fnd_pos2 );

        for( j = 0; j < pw.filled ; j++ )
        {
            if( i >= pw.length ) 
            { 
                offset = ( i - ( ( j + 1 ) * ( fnd_pos2 - fnd_pos1 ) ) ) % pw.length;
                //offset = ( i - ( j * ( fnd_pos2 - fnd_pos1 ) ) - ( fnd_pos2 - fnd_pos1 )  ) % pw.length;
            }
            else
            {
                offset = i - ( j * ( fnd_pos2 - fnd_pos1 ) ) ;
            }

            qual = elem->maq[read][offset];         
            p_err = pow( (double)0.1, (qual/10.0) );
            p_acc += (1 - p_err);
            if( qual > 0 )
            {
                cvg++;
            }
            //fprintf( stderr, "%s elem(%p) id(%d) start_pos:%d(%c) offset(%d) (%d/%d), qual[%d]:%d, p_err:%.4f, acc:%.4f cvg(%d)\n", \
                             INFO_015, elem, elem->id, elem->pos, elem->base, offset, j + 1, pw.filled, read, elem->maq[read][offset], p_err, p_acc, cvg );
            elem = elem->next;
        }

        if( cvg <= 0 )
        {
            gms = 0.0;
            cvg = 0;
        }
        else 
        {
            gms = (p_acc / cvg) * 100;
        }

        if(  pw.tail->pos == (i + 1)  )
        { 
            fprintf( stderr, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i+1, pw.tail->base, cvg, gms );
            fprintf( stdout, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i+1, pw.tail->base, cvg, gms );
        }
        else
        {
            fprintf( stderr, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i+1, '*', cvg, gms );
            fprintf( stdout, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i+1, '*', cvg, gms );
        }
    }
}

/*
static void compute_gms( prob_elem * head, char *chr, int fnd_pos1, int fnd_pos2 )
{
    circulate_window_list( head, READ1, chr, fnd_pos1, fnd_pos2 );
}
*/

void prob_long_fill_elem( prob_elem * pb, 
                     int org_pos, int fnd_pos1, int fnd_pos2,
                     char base, int read, int qual, int flag  )
{

    int i = 0;
    
    pb->pos = org_pos; 
    pb->base = base; 

    if( ( flag & 0x0040 ) || ( flag & 0x0080 ) )
    {

    }
    else if( ( flag & 0x10 ) || ( flag == 0 ) || ( flag == 0x4 )  )  // if flag == 0, it's single end read or cannot  know which read if comes from if paired-end read
    {
        if( pb->flag == -1 )
        {
            fprintf( stderr, "%sL fill [%d,%d] with qual(%d)\n", INFO_016, fnd_pos1, fnd_pos2, qual );

            for( i = (fnd_pos1-org_pos); i < (fnd_pos2-org_pos+1) ; i++ )
            //for( i = 0; i < length ; i++ )
            {

                if ( pb->maq[READ1][i] != 0 )
                {
                     pb->maq[READ1][i] = (pb->maq[READ1][i] + qual)/2;
                }
                else 
                {
                     pb->maq[READ1][i] = qual;
                }
            }
        }
        else
        {
            fprintf( stderr, "[ERROR:004] prob_long_check_fill_elem: flag: not first, not second\n" );
        }
    }
    else 
    {
        fprintf( stderr, "[ERROR:005] flag(%d) \n", flag );
    }
}

void prob_long_check_fill_elem( prob_elem * pb, 
                           char *chr, int org_pos, int fnd_pos1, int fnd_pos2, 
                           char base, int read, int qual, int flag  )
{

    fprintf( stderr, "%sL pw.head->pos:%d pw.tail->pos:%d, org_pos:%d\n", INFO_017, pw.head->pos, pw.tail->pos, org_pos );
    
    if( pw.head->pos == 0 )  
    {
        prob_long_fill_elem( pw.head, org_pos, fnd_pos1, fnd_pos2, base, read, qual, flag );
        pw.filled++;
        pw.tail = pw.head;
        fprintf( stderr, "%sL case 1: pw.filled:%d (%d - %d)\n", INFO_018, pw.filled, pw.head->pos, pw.tail->pos );
    }
    else// if( pw.head->pos != 0 )
    {
        if( pw.tail->pos == org_pos) 
        {
            prob_long_fill_elem( pw.tail, org_pos, fnd_pos1, fnd_pos2, base, read, qual, flag );
            fprintf( stderr, "%sL case 2: pw.filled:%d (%d - %d)\n", INFO_019, pw.filled, pw.head->pos, pw.tail->pos );
        }
        else if( pw.tail->pos < org_pos )
        {    
            fprintf( stderr, "%sL pw.tail->next: %p, pw.head->pos: %d, pw.filled:%d, pw.size:%d\n",
                              INFO_020, pw.tail->next, pw.head->pos, pw.filled, pw.size );

            if( pw.filled < pw.size) 
            {
                prob_long_fill_elem( pw.tail->next, org_pos, fnd_pos1, fnd_pos2, base, read, qual, flag );
                pw.tail = pw.tail->next;
                pw.filled++;
                fprintf( stderr, "%sL case 3: pw.filled:%d (%d - %d), pw.tail->id: %d\n", INFO_022, pw.filled, pw.head->pos, pw.tail->pos, pw.tail->id );
            }
            else //if( (pw.head->pos + pw.head->size) <= org_pos )
            {
                prob_init_elem( pw.head, pw.size );
                pw.tail->next = pw.head; 
                pw.head = pw.head->next;

                prob_long_fill_elem( pw.tail->next, org_pos, fnd_pos1, fnd_pos2, base, read, qual, flag );
                pw.tail = pw.tail->next;
                pw.tail->next = NULL;

                fprintf( stderr, "%sL case 4: pw.filled:%d (%d - %d), pw.tail->id:%d \n", INFO_023, pw.filled, pw.head->pos, pw.tail->pos, pw.tail->id );
            }
        }
        else
        {
            fprintf( stderr, "[INFO:MUST] case 5: pw.filled:%d, pw.tail->pos:%d, org_pos:%d\n", pw.filled, pw.tail->pos, org_pos );

        }
    }
    // for debuging
    //prob_print_elem( length );
}

int prob_long_fill_window( FILE * output, int distance, char *chr, 
                      int org_pos, int fnd_pos1, int fnd_pos2, 
                      char base, int flag, int qual )
{
    fprintf( stderr, "%sL chr: %s, pos:%d(%d-%d), base: %c, flag: 0x%x qual: %d\n", 
                     INFO_024, chr, org_pos, fnd_pos1, fnd_pos2, base, flag, qual );

    if( ( flag & 0x0040 ) && ( pw.head->maq[READ1][FST] == -1 ) ) // the first read1
    {
        prob_long_check_fill_elem( pw.head, chr, org_pos, fnd_pos1, fnd_pos2, base, READ1, qual, flag );
    }
    else if( (flag & 0x0040) && ( pw.head->maq[READ1][FST] != -1 ) ) // the second read1
    {
        prob_long_check_fill_elem( pw.head, chr, org_pos, fnd_pos1, fnd_pos2, base, READ1, qual, flag );
    }
    else if( ( flag & 0x0080 ) && ( pw.head->maq[READ2][FST] == -1 ) ) // the first read2
    {
        prob_long_check_fill_elem( pw.head, chr, org_pos, fnd_pos1, fnd_pos2, base, READ2, qual, flag );
    }
    else if( (flag & 0x0080) && ( pw.head->maq[READ2][FST] != -1 ) ) // the second read2
    {
        prob_long_check_fill_elem( pw.head, chr, org_pos, fnd_pos1, fnd_pos2, base, READ2, qual, flag );
    }
    else if( ( flag == 0 ) || ( flag & 0x10 ) || ( flag & 0x4) )// single-end read, unmapped
    {
        fprintf( stderr, "%sL pos:(%s)%d-%d(%c), flag:0x%x(single-end) qual: %d\n", INFO_021, chr, fnd_pos1, fnd_pos2, base, flag, qual);
        prob_long_check_fill_elem( pw.head, chr, org_pos, fnd_pos1, fnd_pos2, base, -1, qual, flag );
    }
    else if( ( fnd_pos1 - pw.head->pos ) == 1 )
    {
        fprintf( stderr, "[ERROR] here\n" );
        prob_long_check_fill_elem( pw.head, chr, org_pos, fnd_pos1, fnd_pos2, base, -1, qual, flag );  //flag
    }
    else
    {
        fprintf( stderr, "[ERROR] here\n" );
    }

    return 0;
}


    
int prob_long_move_window( FILE * output, int distance, char *org_chr, 
                      int org_pos, int fnd_pos1, int fnd_pos2, 
                      char base, int flag, int qual )
{
//    compute_gms( pw.head, org_chr, fnd_pos1, fnd_pos2 );
    circulate_window_list( pw.head, READ1, org_chr, fnd_pos1, fnd_pos2 );

    return 0;
}

static void cleanup_window_list( prob_elem * hd, int read, char *chr, int fnd_pos1, int fnd_pos2 )
{
    int i = 0, j = 0;
    int qual = 0;
    int cvg = 0;

    double p_err = 0.0;
    double p_acc = 0.0;
    double gms = 0.0;

    int offset = 0;

    prob_elem * elem = pw.head;

    fprintf( stderr, "\nStart cleanup\n" );
    fprintf( stderr, "%sL pos1:%d, pos2(%d)\n", INFO_028, fnd_pos1, fnd_pos2 );

    for( i = fnd_pos1-1; i < fnd_pos2-1; i++ )
    {
        elem = pw.head;
        p_acc = 0.0;
        p_err = 0.0;
        gms = 0.0;
        cvg = 0;

        //fprintf( stderr, "%sL pw.head->id(%d), pw.tail->id(%d) i(%d), (%d-%d)\n", INFO_013, pw.head->id, pw.tail->id, i, fnd_pos1, fnd_pos2 );

        for( j = 0; j < pw.filled ; j++ )
        {
            if( i >= pw.length )
            {
                offset = ( i - ( ( j + 1 ) * ( fnd_pos2 - fnd_pos1 ) ) ) % pw.length;
                //offset = ( i - ( j * ( fnd_pos2 - fnd_pos1 ) ) - ( fnd_pos2 - fnd_pos1 )  ) % pw.length;
            }
            else
            {
                offset = i - ( j * ( fnd_pos2 - fnd_pos1 ) ) ;
            }

            qual = elem->maq[read][offset];
            p_err = pow( (double)0.1, (qual/10.0) );
            p_acc += (1 - p_err);
            if( qual > 0 )
            {
                cvg++;
            }
            //fprintf( stderr, "%s elem(%p) id(%d) start_pos:%d(%c) offset(%d) (%d/%d), qual[%d]:%d, p_err:%.4f, acc:%.4f cvg(%d)\n", \
                             INFO_015, elem, elem->id, elem->pos, elem->base, offset, j + 1, pw.filled, read, elem->maq[read][offset], p_err, p_    acc, cvg );
            elem = elem->next;
        }

        if( cvg <= 0 )
        {
            gms = 0.0;
            cvg = 0;
        }
        else
        {
            gms = (p_acc / cvg) * 100;
        }

        if(  pw.tail->pos == (i + 1)  )
        {
            fprintf( stderr, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i+1, pw.tail->base, cvg, gms );
            fprintf( stdout, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i+1, pw.tail->base, cvg, gms );
        }
        else
        {
            fprintf( stderr, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i+1, '*', cvg, gms );
            fprintf( stdout, "%s\t%09d\t%c\t%d\t%.2f\n", chr, i+1, '*', cvg, gms );
        }
    }

    pw.filled--;
    pw.head = pw.head->next;

}



void prob_long_clean_windows( FILE * output, char * org_chr, int org_pos )
{
    int i = 0;
    int term = pw.length/pw.size;

    prob_elem * head = pw.head;

    for( i = 0; i < pw.size; i++ )
    {  
        cleanup_window_list( pw.head, READ1, org_chr, org_pos + (i*term), org_pos + ((i+1)*term) );
    }

    prob_destroy_window( head );
    
}


