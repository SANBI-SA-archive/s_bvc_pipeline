#include <stdio.h> 
#include <string.h>

#include "../inc/sam.h"  
#include "analyzer_common.h"
#include "analyzer_short.h"
#include "prob_common.h"
#include "prob_short.h"
#include "resource.h"

void analyzer_short(int argc, char *argv[])  
{  
    char input[BUF_SIZE] = { 0, };
    int length = 0;
    int distance = 0;
    char tech[256] = { 0, };

//    FILE *output dd= NULL;

    char org_chr[16] = { 0, };
    char prev_chr[16] = { 0, };
    int  org_pos;
    int  prev_pos = 1;
    int  prev_pos1 = 0;
    int  is_new_pos = true;  // HERE
    char fnd_chr[16] = { 0, };
    int  fnd_pos1;
    int  fnd_pos2;
    int  fnd_len;
    char base;
    uint32_t  flag;
    int  qual;
    int  ret;
    char *ARGV[ARGC_MAX];
    int ARGC = 0;
    //int i = 0;

    if( argc == 0 ) // HADOOP
    {
        ARGV[0] = getenv("mapred_job_arg0"); // e.g. 50
        ARGV[1] = "analyzer";
        ARGV[2] = getenv("mapred_job_arg2"); // e.g. 50
        ARGV[3] = getenv("mapred_job_arg3"); // e.g. -e
        ARGV[4] = getenv("mapred_job_arg4"); // e.g. 0.02
        ARGV[5] = getenv("mapred_job_arg5"); // e.g. -q
        ARGV[6] = getenv("mapred_job_arg6"); // e.g. A
        ARGV[7] = getenv("mapred_job_arg7"); // e.g. -r
        ARGV[8] = getenv("mapred_job_arg8"); // e.g. 200
        ARGV[9] = getenv("mapred_job_arg9"); // e.g. -t
        ARGV[10] = getenv("mapred_job_arg10"); // e.g. 20
        ARGV[11] = getenv("mapred_job_arg11"); // e.g. -f
        ARGV[12] = getenv("mapred_job_arg12"); 
        ARGV[13] = getenv("mapred_job_arg13"); 
        ARGV[14] = getenv("mapred_job_arg14"); 
        ARGV[15] = getenv("mapred_job_arg15"); 
        ARGV[16] = getenv("mapred_job_arg16"); 
        ARGV[17] = getenv("mapred_job_arg17"); 
        ARGV[18] = getenv("mapred_job_arg18"); 
        ARGV[19] = getenv("mapred_job_arg19"); 
        ARGV[20] = getenv("mapred_job_arg20"); 
        ARGV[21] = getenv("mapred_job_arg21"); 
        ARGV[22] = getenv("mapred_job_arg22"); 
        ARGV[23] = getenv("mapred_job_arg23"); 

        fprintf( stderr, "0. %s\n", ARGV[0] );
        fprintf( stderr, "1. %s\n", ARGV[1] );
        fprintf( stderr, "2. %s\n", ARGV[2] );
        fprintf( stderr, "3. %s\n", ARGV[3] );
        fprintf( stderr, "4. %s\n", ARGV[4] );
        fprintf( stderr, "5. %s\n", ARGV[5] );
        fprintf( stderr, "6. %s\n", ARGV[6] );
        fprintf( stderr, "7. %s\n", ARGV[7] );
        fprintf( stderr, "8. %s\n", ARGV[8] );
        fprintf( stderr, "9. %s\n", ARGV[9] );
        fprintf( stderr, "10. %s\n", ARGV[10] );
        fprintf( stderr, "11. %s\n", ARGV[11] );
        fprintf( stderr, "12. %s\n", ARGV[12] );
        fprintf( stderr, "13. %s\n", ARGV[13] );
        fprintf( stderr, "14. %s\n", ARGV[14] );
        fprintf( stderr, "15. %s\n", ARGV[15] );
        fprintf( stderr, "16. %s\n", ARGV[16] );
        fprintf( stderr, "17. %s\n", ARGV[17] );
        fprintf( stderr, "18. %s\n", ARGV[18] );
        fprintf( stderr, "19. %s\n", ARGV[19] );
        fprintf( stderr, "20. %s\n", ARGV[20] );
        fprintf( stderr, "21. %s\n", ARGV[21] );
        fprintf( stderr, "22. %s\n", ARGV[22] );
        fprintf( stderr, "23. %s\n", ARGV[23] );

        ARGC = atoi( ARGV[0] );
 
        parse_args( ARGC, ARGV, &length, &distance, tech );
    }
    else
    {
        parse_args( argc, argv, &length, &distance, tech );
    }

    fprintf( stderr, "==================================================\n" );
    fprintf( stderr, "Analyzer for short reads\n" );
    fprintf( stderr, "Seq tech : %s\n", tech );
    fprintf( stderr, "read length : %d\n", length );
    fprintf( stderr, "library distance : %d\n", distance );
    fprintf( stderr, "==================================================\n" );

    //fprintf( stdout, "#chr\tpos\t\tbase\tmaq\ttotal = >= + <(um)\tGMS\n");
    fprintf( stdout, "#chr\tpos\t\tbase\tcov\tGMS\n");


    prob_init_window( 100, length );
//    output = fopen( "sort.gma", "w+" );

    while( fgets( input, BUF_SIZE-1, stdin ) )
    {
        //fprintf( stderr, "%s", input );
        get_info( input, org_chr, &org_pos, 
                         fnd_chr, &fnd_pos1, &fnd_pos2, &fnd_len, 
                         &base, &flag, &qual, &ret ); 

        fprintf( stderr, "\norigin(%s:", org_chr );
        fprintf( stderr, "%d)", org_pos );
        fprintf( stderr, "%s:", fnd_chr );
        fprintf( stderr, "%d-", fnd_pos1 );
        fprintf( stderr, "%d", fnd_pos2 );
        fprintf( stderr, "(%d)\t", fnd_len );
        fprintf( stderr, "%c:", base );
        fprintf( stderr, "%d(0x%x):", flag, flag );
        fprintf( stderr, "%d:", qual );
        fprintf( stderr, "%d\n", ret );


        if( strcmp( prev_chr, "" ) == 0 )  // start
        {
            if( is_same_chr( org_chr, fnd_chr ) == true )      
            {
                fprintf( stderr, "none -> %s +\n", org_chr );
                strcpy( prev_chr, org_chr );
            }
            else
            {
                fprintf( stderr, "[INFO] the first aligment is incorrect (org_chr:%s, fnd_chr:%s)\n", org_chr, fnd_chr );
                strcpy( prev_chr, org_chr );
            }
        }
        else if( strcmp( prev_chr, org_chr ) == 0 ) 
        {
            if( is_same_chr( org_chr, fnd_chr ) == true )      
            {
                if( prev_pos != org_pos )
                {
                    fprintf( stderr, "%s prev_pos:%d, org_pos:%d\n", INFO_001, prev_pos, org_pos );
                    prob_short_move_window( NULL,
                                     0, // distance
                                     org_chr, 
                                     org_pos,
                                     prev_pos, //org_pos,
                                     org_pos, //org_pos,
                                     base, //base,
                                     0,   //flag,
                                     -1,  //qual, 
                                     length
                                     );
     
                    prev_pos = org_pos;
                    prev_pos1 = fnd_pos1; 
                    is_new_pos = true;
                }
                else
                {
                    if( prev_pos1 == fnd_pos1 )
                    {
                        //fprintf( stderr, "%s fnd_pos1: %d, prev_pos1: %d\n", INFO_002, fnd_pos1, prev_pos1 );
                        if ( strcmp( tech, "pacbio" ) == 0 ) 
                        {    
                            is_new_pos = true;  // for pacbio, is_new_pos should be true, all the time
                        }
                    }
                    else 
                    {  
                        is_new_pos = true;
                    }
                }
            }
            else 
            {
                //fprintf( stderr, "[INFO] prev_chr:%s, org_chr:%s, fnd_chr:%s\n", prev_chr, org_chr, fnd_chr );
                //will be ignored in the next step
            }
        }
        else // new chromosome
        {
            fprintf( stderr, "[INFO:MUST] clear windows: prv_chr(%s), prv_pos(%d+1)\n", prev_chr, prev_pos );
            fprintf( stderr, "[INFO:MUST] clear windows: org_chr(%s), org_pos(%d)\n", org_chr, org_pos );

            prob_short_clean_windows( NULL, prev_chr, prev_pos );  // NULL means stdout
            //prob_destroy_window( NULL );
            prob_init_window( 100, length );

            fprintf( stderr, "%s -> %s *\n", prev_chr, org_chr );
            is_new_pos = true;
            strcpy( prev_chr, org_chr );
        }

        // check chromosome avilability

        if( is_same_chr( org_chr, fnd_chr ) == true )      
        {
            fprintf( stderr, "%s org_pos(%d) <= fnd_pos1(%d) && fnd_pos2(%d) < (org_pos + legnth)%d\n", 
                             INFO_027, org_pos, fnd_pos1, fnd_pos2, (int)(org_pos + length )  );
            // check position availability

            if( ( (org_pos <= fnd_pos1) && ( (fnd_pos2-1) < (org_pos + length ) ) ) ||
                ( fnd_pos1 == 0 && fnd_pos2 == 99 ) )
            {
                if( is_new_pos == true )
                {
//                    fprintf( stderr, "%s new pos\n", INFO_004 );
                    prob_short_fill_window( NULL,
                                 distance,
                                 org_chr,  // org_chr = fnd_chr 
                                 org_pos, 
                                 fnd_pos1, 
                                 fnd_pos2,
                                 base,
                                 flag,
                                 qual,
                                 length
                                 );
                }
                else
                {
                    fprintf( stderr, "%s not a new pos\n", INFO_005 );
                    prob_short_move_window( NULL,
                                 distance,
                                 org_chr,
                                 org_pos, 
                                 fnd_pos1,
                                 fnd_pos2,
                                 base,
                                 flag,
                                 qual, 
                                 length 
                                 );
                }
            }
            else
            {
                fprintf( stderr, "%s misaligned read\n", INFO_030 );
                prob_short_fill_window( NULL,
                                        distance,
                                        org_chr,  // org_chr = fnd_chr 
                                        org_pos, 
                                        org_pos, 
                                        org_pos + length - 1,
                                        '*',
                                        flag,
                                        0,
                                        length
                                        );
            }

        }
        else // diff chromosome
        {
            fprintf( stderr, "ERR %s diff %s != %s, pos(org:%d, fnd:%d-%d)\n", INFO_006, org_chr, fnd_chr, org_pos, fnd_pos1, fnd_pos2 );
            prob_short_fill_window( NULL,
                              distance,
                              org_chr,  // org_chr = fnd_chr 
                              org_pos, 
                              org_pos, 
                              org_pos + length - 1,
                              '*',
                              flag,
                              0,
                              length
                              );
        }
    } // while

    fprintf( stderr, "%s cleanup: org_chr(%s), org_pos(%d), length(%d)\n", INFO_032, org_chr, org_pos, length );
    prob_short_clean_windows( NULL, org_chr, org_pos ); 
    fprintf( stderr, "%s destroy window\n", INFO_032 );
    //prob_destroy_window( NULL );
}



