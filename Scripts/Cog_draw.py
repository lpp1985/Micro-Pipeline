#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/1/23
"""
import sys,os

commandline = """
#!/usr/local/bin/Rscript
require(ggplot2)
library(grid)
exampleFile = "%s"
countsTable <- read.delim( exampleFile, header=TRUE, stringsAsFactors=TRUE )
aa<-ggplot(countsTable)+geom_bar(aes(x=COG.Category, fill=COG.Category),show_guide =FALSE)+coord_flip()+ylab("Gene Number")
png("%s", width=1024, height=512,type="cairo")
aa <- ggplot_gtable(ggplot_build(aa))
grid.draw(aa)
dev.off()


"""%(sys.argv[1],sys.argv[2])
SCRIPT = open(sys.argv[3],'w')
SCRIPT.write(commandline)
SCRIPT.close()
os.system("Rscript %s"%(sys.argv[3]))
