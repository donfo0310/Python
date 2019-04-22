# RでXBRLデータを取得してみた
# http://horihorio.hatenablog.com/entry/2014/12/15/235107

rm(list=ls())
invisible(gc()); invisible(gc())

# library
library("RCurl")
library("XML")
library("plyr")

# Get Securities-Code
tmp.list <- paste0("D:\\OneDrive\\ドキュメント\\Project\\Python\\FinancialAnalysis\\master\\TSE1.csv", dir("./master/", pattern = "TSE1.csv") )
tmp.master.SIC <- list()
master.SIC     <- c()

# csv-path list
for (i in 1:length(tmp.list)) {
  
  mkt.name <- sub(".txt", "", unlist(strsplit(tmp.list[i], "/"))[3])  # ex. TSE1
  tmp.master.SIC[[i]] <- read.table(tmp.list[i], sep = "\t", header = TRUE, stringsAsFactors = FALSE)
  tmp.master.SIC[[i]] <- cbind( mkt.name, tmp.master.SIC[[i]] )
  master.SIC <- rbind(master.SIC, tmp.master.SIC[[i]][1:6])
}
colnames(master.SIC) <- sub("X","",colnames(master.SIC))
rm(list=c("i", "mkt.name", ls(pattern = "tmp*"))) # cleanup

# Output Securities-Code
write.table(master.SIC, "./master/master_SIC.txt", sep = "\t", col.names = TRUE, row.names = TRUE)

# Get XBRL
# Get Ready
# Securities-Code As Query param
SICs <- as.character(master.SIC$コード) #SIC.code

## Download XBRL files to 'data' folder
# Create folder.
dir.create("data")

# Set Const
api.service.url <- "http://resource.ufocatch.com/atom/edinetx" # API-URI

# set date from-to
date.from <- as.Date('2013/6/1')
date.to   <- as.Date('2013/6/30')

# Get XBRL
for (strSIC in SICs[1:1]){

  Sys.sleep(10)
  
  # Send Request
  strURL <- paste0(api.service.url, "/query/", strSIC) # Concat 'URI' 'Securities-Code'
  Sys.sleep(1)

  # Get res
  objQuery <- httpGET(strURL) 
  
  # Exchange API-Response to XMLInternalDocument from xmlParse
  objXML <- xmlParse(objQuery,encoding="UTF-8")
  # Get namespace as vector(simplify=TRUE)
  objXML.namespaces <- xmlNamespaceDefinitions(objXML,simplify=TRUE)
  # set void pre-fix to dafault namespase
  names(objXML.namespaces)[ names(objXML.namespaces)=="" ] <- "default"
  
  # element-node: Specify entry
  nodes.entry <- getNodeSet(objXML,"//default:entry",namespaces=objXML.namespaces)
  # Extract Only Yuho
  lst.YUHO <- list()

  # proc <entry> tag
  for(node in nodes.entry){

    lst.temp <- list()
    # Get <title> tag
    title.value <- xpathSApply(node,path="default:title",fun=xmlValue,namespaces=objXML.namespaces)
    # is yuho? *yukashokenhoukokusho*
    is.YUHO <- grepl(pat="*有価証券報告書*",x=title.value)

    if(is.YUHO){
      
      # operand as 'Filing date' teishutubi
      is.date <- xpathSApply(node,path="default:updated",fun=xmlValue,namespaces=objXML.namespaces)
      is.date <- as.Date(substr(is.date, 1, 10))

      if (date.from <= is.date && is.date <= date.to) {
        # Get ID
        lst.temp$id <- xpathSApply(node,path="default:id",fun=xmlValue,namespaces=objXML.namespaces)
        lst.temp$title <- title.value
        # Get href as type='application/zip' from <link> tag
        lst.temp$url <- xpathSApply(node,path="default:link[@type='application/zip']/@href",namespaces=objXML.namespaces)
        lst.YUHO[[lst.temp$id]] <- lst.temp
      }

    }
  }
  
  # Save XBRL
  # change df from plyr.ldply()
  dat.export <- ldply(lst.YUHO,.fun=data.frame)[, -1]
  
  if(!sum(dim(dat.export))==0){ # 該当なしの場合は抜ける
    for(lst in lst.YUHO){
      temp <- getBinaryURL(url=lst$url ) # this is binary
      writeBin( temp, paste0("data/",lst$id,".zip") ) # save zip
    }
    dat.export <- cbind(strSIC, substr(dat.export$title, 2, 7), dat.export)
    write.table(dat.export, file = "downloaded_XBRL.txt", sep = "\t", append = TRUE, row.names = FALSE, col.name = FALSE)
  }
}

rm(list = ls()) # cleanup