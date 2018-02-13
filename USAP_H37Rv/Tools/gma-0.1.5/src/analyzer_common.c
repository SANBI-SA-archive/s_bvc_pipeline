#include <stdio.h> 
#include <string.h>
#include <stdbool.h>

#include "../inc/sam.h"  
#include "analyzer_common.h"
//#include "prob_common.h"
#include "resource.h"


void get_info( char * input, 
               char *org_chr, int *org_pos, 
               char *fnd_chr, int *fnd_pos1, int *fnd_pos2, int *fnd_len, 
               char *base, unsigned int *flag, int *qual, int *ret )
{  
    char * tmp;
    //fprintf( stderr, "%s", input );

    tmp = (strtok( input, "|:\t\n" ) );
    strcpy( org_chr, tmp );

    tmp = strtok( NULL, "(\t\n" );
    if( tmp != NULL )
    {
        *org_pos = atoi( tmp );
    }else
    {   *org_pos = -1;
    }

    tmp = strtok( NULL, ":\t\n" );

    tmp = (strtok( NULL, ":\t\n" ) );
    strcpy( fnd_chr, tmp );

    tmp = strtok( NULL, ":-()\t\n" );
    if( tmp != NULL )
    {
        *fnd_pos1 = atoi( tmp );
    }else
    {   *fnd_pos1 = -1;
    }

    tmp = strtok( NULL, ":-()\t\n" );
    if( tmp != NULL )
    {
        *fnd_pos2 = atoi( tmp );
    }else
    {   *fnd_pos2 = -1;
    }

    tmp = strtok( NULL, ":-()\t\n" );
    if( tmp != NULL )
    {
        *fnd_len = atoi( tmp );
    }else
    {   *fnd_len = -1;
    }

    tmp = (strtok( NULL, " :\t\n" ) );
    if( tmp != NULL )
    {   *base = (*tmp);
    }
    else
    {
        *base = 'N';
    }

    tmp = strtok( NULL, ":\t\n" );
    if( tmp != NULL )
    {
        //*flag = atoi( &tmp[2] ); // 0x remove
        *flag = atoi( tmp ); // 0x remove
    }else
    {   *flag = -1;
    }

    tmp = strtok( NULL, ":\t\n" );
    if( tmp != NULL )
    {
        *qual = atoi( tmp );
    }else
    {
        *qual = -1;
    }

    tmp = strtok( NULL, ":\t\n" );
    if( tmp != NULL )
    {
        *ret = atoi( tmp );
    }else
    {
        *ret = -1;
    }

/*
    fprintf( stderr, "%d:", *org_pos );
    fprintf( stderr, "%d:", *fnd_pos1 );
    fprintf( stderr, "%d:", *fnd_pos2 );
    fprintf( stderr, "%d:", *fnd_len );
    fprintf( stderr, "%c:", *base );
    fprintf( stderr, "%d:", *flag );
    fprintf( stderr, "%d:", *qual );
    fprintf( stderr, "%d\n", *ret );
*/

}

int parse_args( int argc, char *argv[],
                int *length, int *distance, char *tech )
{
    int ret = 0;
    char c;

    // all options need their value
    while( ( c = getopt( argc, argv, "l:q:s:i:d:o:t:f:b:x:m:p:" )) >= 0 )
    {
        //fprintf( stderr, "optind : %d, %s\n", optind, optarg );

        switch(c)
        {
        case 'l': (*length) = atoi( optarg ); break;
        case 'q': break; //(*qual) = optarg[0]; break;
        case 's': break; //(*err_rate) = atof( optarg ); break;
        case 'i': break;
        case 'd': break; //(*err_rate) = atof( optarg ); break;
        case 'o': (*distance) = atoi( optarg); break; //(*distance) = atoi( optarg); break;
        case 't': strcpy( tech, optarg ); break; //(*distance) = atoi( optarg); break;
        case 'f': break; //strcpy( fasta, optarg); break;
        case 'b': break; //strcpy( fasta, optarg); break;
        case 'x': break; //strcpy( fasta, optarg); break;
        case 'm': break;
        case 'p': break; //strcpy( fasta, optarg); break;
        default : fprintf( stderr, "%s: WRONG OPTION \'%c\'\n", __FILE__, c );
                  ret = -1;
                  break;
        }
    }
    optind = 1;
    return ret;
}

bool is_same_chr( char* chr1, char *chr2 )
{
    if( strcmp( chr2, "*" ) == 0 )
    {
        return true;
    }
    else if( ( strcmp( &chr1[3],  chr2 )    == 0 ) ||
             ( strcmp( &chr1[3], &chr2[3] ) == 0 ) ||
             ( strcmp(  chr1   ,  chr2    ) == 0 ) ||
             ( strcmp(  chr1   , &chr2[3] ) == 0 ) )
    {
        return true;
    }
    else
    {
        return false;
    }
}






