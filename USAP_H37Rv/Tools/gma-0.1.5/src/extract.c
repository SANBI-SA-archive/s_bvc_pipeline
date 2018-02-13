#include <stdio.h> 
#include <zlib.h>

#include "../inc/sam.h"  
#include "extract.h"
#include "resource.h"
#include "kseq.h"


KSEQ_INIT( gzFile, gzread );

typedef struct 
{  
    int beg, end;  
    samfile_t *in;  

} anal_t;  
  
// callback for bam_fetch()  
/*
static int fetch_func(const bam1_t *b, void *data)  
{  
    bam_plbuf_t *buf = (bam_plbuf_t*)data;  
    bam_plbuf_push(b, buf);  
    return 0;  
} 
*/ 
// callback for bam_plbuf_init()  


static int pileup_func(uint32_t tid, uint32_t pos, int n, const bam_pileup1_t *pl, void *data)  
{  
    // as a callback function
/*
    anal_t *input = (anal_t*)data; 
    if ((int)pos >= input->beg && (int)pos < input->end)  
        fprintf( stderr, "%s\t%d\t%d\n", input->in->header->target_name[tid], pos + 1, n);  
*/
    return 0;  
}  



int find_chr( char *name, kseq_t *seq, char *chr )
{
    int l;
    int ret = -1;

    while( (l=kseq_read( seq )) >= 0 )
    {
    
        fprintf( stderr, "name : %s, seq->name.s: %s\n", name, seq->name.s );

        if( strcmp( name, seq->name.s ) == 0 )
        {
            strcpy( chr, seq->name.s );
            ret = 0;
            break;
        }
    }
    return ret;
    
}

void int2bit(int num)
{
    if( num > 0 )
    {
        int2bit(num/2);
        fprintf( stderr, "%d", num%2 );
    }
    return;
}


static int counter = 0;

void print_lower4bit(int num)
{
    if( counter < 4 )
    {
        counter++;
        print_lower4bit(num/2);
        fprintf( stderr, "%d", num%2 );
    }
    return;
}

void get_cigar( int num, char *op, int *len ) 
{
    //int2bit( num );
    //fprintf( stderr, "\t");

    //counter = 0;
    //print_lower4bit( num );
    (*len) = (num & 0xFFFFFFF0)/16;

    switch( num & 0xF ) 
    {
    case 0: (*op) = 'M';  break;
    case 1: (*op) = 'I';  break;
    case 2: (*op) = 'D';  break;
    case 3: (*op) = 'N';  break;
    case 4: (*op) = 'S';  break;
    case 5: (*op) = 'H';  break;
    case 6: (*op) = 'P';  break;
	case 7: (*op) = '=';  break;
	case 8: (*op) = 'X';  break;
    default: fprintf( stderr, "%s cigar operation code is not supported\n", ERR_001 ); 
             break; 
    }
    //int2bit( num & 0xfffffff0 );

}


void parse_bam( char *tech, char *ref, int length, int start_base_pos, const char *bam )
{  
    anal_t input;  
    gzFile pRef;
    kseq_t * seq = NULL;
    char chr[8] = { 0, };
    int ret;
    bam_plbuf_t *buf;
    bam1_t *b;
    uint32_t *cigar = NULL;
    char op = ' ';
    int len1 = 0, len = 0;
    int j = 0;
/*
    fprintf( stderr, "ref: %s\n", ref );
    fprintf( stderr, "length: %d\n", length );
    fprintf( stderr, "start_base_pos: %d\n", start_base_pos );
    fprintf( stderr, "bam: %s\n", bam );
*/
    input.beg = 0; input.end = 0x7fffffff;  
    input.in = samopen(bam, "rb", 0);
  
    if (input.in == 0) 
    {  
        fprintf(stderr, "Fail to open BAM file %s\n", bam);  
        return;  
    }  

    pRef = gzopen( ref, "r" );

    if( pRef == NULL )
    {
        fprintf( stderr, "ref : %s\n", ref );
        fprintf( stderr, "pRef: %p\n", pRef );

        return;
    }

    seq = kseq_init( pRef );

    b = bam_init1(); // alloc memory size of bam1_t
    buf = bam_plbuf_init(pileup_func, &input); // alloc memory

    bam_plbuf_set_mask(buf, -1);
    
    while ((ret = samread( input.in, b)) >= 0)
    {   
        bam_plbuf_push(b, buf); 
        
        if( b->core.flag & 0x0004 ) // unmapped
        {    // do nothing
/*
            qname1 = strtok(bam1_qname(b), ":\t\n ");
            qname2 = strtok(NULL, ":\t\n ");
            qname3 = atoi(qname2);

            fprintf( stderr, "%s:%10d:%s:%d\t%c:%d:%d:%d\n", 
                qname1, qname3, "*", b->core.pos,
                '*', b->core.flag, b->core.qual, ret );
*/
/*
 *          fprintf( stdout, "%s:%s:%d\t%c:0x%x:%d:%d\n", 
                bam1_qname(b), "*", b->core.pos+1,
                '*', b->core.flag, b->core.qual, ret );
*/
            fprintf( stdout, "%s:%s:%09d-%09d(%d)\t%c:%d:%d:%d\n", 
                    bam1_qname(b),
                    "*",
                    b->core.pos+1, b->core.pos+len, len,
                    '*', b->core.flag, b->core.qual, ret );
/*
            fprintf( stderr, "%s:%s:%d\t%c:0x%x:%d:%d\n", 
                bam1_qname(b), "*", b->core.pos,
                '*', b->core.flag, b->core.qual, ret );
*/
        }
        else
        {
            //fprintf( stderr, "n_cigar1: %d, %d, %d, %d\n", b->core.n_cigar, b->l_aux, b->data_len, b->m_data );
            //fprintf( stderr, "qname: %s\t", bam1_qname(b) );
            //int2bit( 13 ); fprintf( stderr, "\n" );
            cigar = bam1_cigar(b);
    
            if( b->core.n_cigar != 0 )
            {
                len = 0;
    
                //int2bit( cigar ); fprintf( stderr, "\n" );
                for( j = 0; j < b->core.n_cigar; j++ )
                { 
                    get_cigar( cigar[j], &op, &len1 ); 
                    //fprintf( stderr, "%d%c ", len1, op );
                    switch( op ) 
                    {
                        case 'M': len += len1; break;
                        case 'I': break;
                        case 'D': break;
                        case 'S': break;
                        default : 
                                  fprintf( stderr, "%s %d%c ", ERR_002, len1, op );
                                  break;
                    }
                }
    
                //get_cigar( cigar[0], &op, &len1 ); 
                //fprintf( stderr, "%d%c\t", len1, op );
                //get_cigar( cigar[b->core.n_cigar-1], &op, &len2);
                //fprintf( stderr, "%d%c (qual(%d)pos(%d)len(%d) : %d-%d)\n", len2, op, b->core.qual, b->core.pos+1, len, len1, b->core.pos+1+len );

                //////////////////////////////////////////////
                if( ( seq != NULL ) &&  
                    ( strcmp( input.in->header->target_name[b->core.tid], chr ) == 0 ) )
                {
                    // already found that 
                    // fprintf( stderr, "found : %s\n", chr );
                }else
                {
                    if( find_chr(input.in->header->target_name[b->core.tid], seq, chr) < 0 )
                    {
                         fprintf( stderr, "%s cannot find chromosome %s\n", \
                                  ERR_003, input.in->header->target_name[b->core.tid] );
                    }else
                    {
                         fprintf( stderr, "FOUND CHR : %s\n", chr );
                    }          
                }
                // remove not aligned to the chromosome
    
                fprintf( stdout, "%s:%s:%09d-%09d(%d)\t%c:%d:%d:%d\n", 
                    bam1_qname(b),
                    input.in->header->target_name[b->core.tid], 
                    b->core.pos+1, b->core.pos+len, len,
                    seq->seq.s[b->core.pos], b->core.flag, b->core.qual, ret );
            }
            else
            {
                fprintf( stderr, "\n" );
            }

/*
            fprintf( stderr, "%s:%s:%d\t%c:%d:%d:%d\n", 
                bam1_qname(b),
                input.in->header->target_name[b->core.tid], 
                b->core.pos,
                seq->seq.s[b->core.pos], b->core.flag, b->core.qual, ret );
*/
        }
    }

    // for the last bases...
  
//    printf("pos:%d(%c), flag:%d qual: %d(ret %d)\n", 
//           b->core.pos+1, seq->seq.s[b->core.pos], b->core.flag, b->core.qual, ret );

    bam_plbuf_push(0, buf); 

    bam_plbuf_destroy(buf); // release memory
    bam_destroy1(b);  // release memory size of bam1_t
     
    samclose(input.in);  
 
    kseq_destroy( seq );
    gzclose( pRef );

    return;  
}  

static int parse_args( int argc, char *argv[],
                char * tech, 
                char * ref,  
                int *length,
                int *start_base_pos, 
                char *bam )
{
    int ret = 0;
    char c;

    // all options need their value
    while( ( c = getopt( argc, argv, "l:q:s:i:d:o:t:f:b:x:m:p:" )) >= 0 )
    {
//        fprintf( stderr, "optind : %d\n", optind );
        switch(c)
        {
        case 'l': (*length) = atoi( optarg ); break;
        case 'q': break;
        case 's': break;
        case 'i': break;
        case 'd': break;
        case 'o': break;
        case 't': strcpy( tech, optarg); break;
        case 'f': strcpy( ref, optarg); break;
        case 'b': break;
        case 'x': break;
        case 'm': strcpy( bam, optarg); break;
        case 'p': break;
        default : fprintf( stderr, "%s:  WRONG OPTION \'%c\'\n", __FILE__, c );
                  ret = -1;
                  break;
        }
    }
    optind = 1;
    return ret;
}



int extract( int argc, char *argv[] )
{

/*
    char *ref = argv[1];
    int length = atoi(argv[2]);
    int start_base_pos = atoi(argv[3]);
    char *bam = argv[4];
*/
    char tech[256] = { 0, };
    char ref[256] = { 0, };
    int length = 0;
    int start_base_pos = 1;
    char bam[256] = { 0, };

    parse_args( argc, argv, tech, ref, &length, &start_base_pos, bam );

    fprintf( stderr, "extract only option\n" );
    fprintf( stderr, "tech: %s\n", tech );
    fprintf( stderr, "ref: %s\n", ref );
    fprintf( stderr, "length: %d\n", length );
    fprintf( stderr, "start_base_pos: %d\n", start_base_pos );
    fprintf( stderr, "bam: %s\n", bam );
    fprintf( stderr, "=============================================\n" );
    
    parse_bam( tech, ref, length, start_base_pos, bam );

    return EXIT_SUCCESS;
} 




