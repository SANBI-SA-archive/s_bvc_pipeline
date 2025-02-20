/** Test routine for reverse complementing Fastq files
 */

/*****************************************************************************
 *****************************************************************************
 *                                                                           *
 *  Copyright (C) 2010 Genome Research Ltd.                                  * 
 *                                                                           *        
 *  Author: Hannes Ponstingl (hp3@sanger.ac.uk)                              *
 *                                                                           *
 *  This file is part of SMALT.                                              *
 *                                                                           *
 *  SMALT is free software: you can redistribute it and/or modify it under   *
 *  the terms of the GNU General Public License as published by the Free     *
 *  Software Foundation, either version 3 of the License, or (at your        *
 *  option) any later version.                                               *
 *                                                                           *
 *  This program is distributed in the hope that it will be useful, but      *
 *  WITHOUT ANY WARRANTY; without even the implied warranty of               *
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU         *
 *  General Public License for more details.                                 *
 *                                                                           *
 *  You should have received a copy of the GNU General Public License along  *
 *  with this program.  If not, see <http://www.gnu.org/licenses/>.          *
 *                                                                           *
 *****************************************************************************
 *****************************************************************************/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "elib.h"
#include "sequence.h"

#define MAXNAMLEN 256
#define OUTPUT_LINEWIDTH 60

int main(int argc, char *argv[])
{
  int errcode = ERRCODE_SUCCESS;
  long ctr = 0L;
  SeqIO *sfp_in, *sfp_out;
  SeqFastq *seqp;
  SeqCodec *codecp;
  ErrMsg *errmsg = 0;

  ERRMSG_CREATE(errmsg);

  if (argc < 3) {
    printf("usage: %s <fasta/fastq file [in]> <fasta/fastq file [out]>\n",argv[0]);
    exit(0);
  }

  if (!(codecp = seqCodecCreate()))
    ERRMSGNO(errmsg, ERRCODE_FAILURE);

  if (!(seqp = seqFastqCreate(0,SEQTYP_UNKNOWN)))
    ERRMSGNO(errmsg, ERRCODE_NOMEM);
  

  sfp_in = seqIOopen(&errcode, argv[1], SEQIO_READ, 0);
  if (!sfp_in) ERRMSGNO(errmsg, errcode);
  
  sfp_out = seqIOopen(&errcode, argv[2], SEQIO_WRITE_FASTQ, 0);
  if (!sfp_out) ERRMSGNO(errmsg, errcode);
  
  while(!(seqIOstatus(sfp_in) || seqIOstatus(sfp_out))) {
    if ((errcode = seqFastqRead(seqp, sfp_in)))
      ERRMSGNO(errmsg, errcode);
    if ((errcode = seqFastqReverse(seqp, codecp)))
      ERRMSGNO(errmsg, errcode);
    if ((errcode = seqFastqWrite(sfp_out, seqp, 0)))
      ERRMSGNO(errmsg, errcode);
    ctr++;
  }
  printf("Revese complement of %li sequences.\n", ctr);
  if (seqIOstatus(sfp_in) != ERRCODE_EOF) ERRMSGNO(errmsg, seqIOstatus(sfp_in));
  if (seqIOstatus(sfp_out)) ERRMSGNO(errmsg, seqIOstatus(sfp_out));

  seqIOclose(sfp_out);
  seqIOclose(sfp_in);

  seqFastqDelete(seqp);
  seqCodecDelete(codecp);

  ERRMSG_END(errmsg);

  return ERRCODE_SUCCESS;
}
  
