# RでXBRLデータを取得してみた
# http://horihorio.hatenablog.com/entry/2014/12/15/235107

# 作業スペースの全オブジェクトを消す（全て消すときはrm(list = ls())）
rm(list=ls())
# 関数 invisible() を使うことで，関数 gc() の実行結果を表示しないようにする。
# 直前の結果を保存している隠しオブジェクト.Last.valueが大きい場合、gc()を2回連続で行なうとよい。
invisible(gc()); invisible(gc())

# library
library("RCurl")
library("XML")
library("plyr")

# Get Securities-Code
# 市場第一部 （内国株）:TSE1
# 市場第二部:TSE2
# マザーズ （内国株）:Mothers
# JASDAQ(グロース）:JQG
# JASDAQ（スタンダード）: JQS

# master ディレクトリのcsvをすべて取得
setwd("D:\\OneDrive\\ドキュメント\\Project\\Python\\Analyze_finance")
tmp.list <- paste0("./master/", dir("./master/", pattern = "*.csv") )

# SIC ... Standard Industrial Classification 産業分類コード
tmp.master.SIC <- list()
master.SIC     <- c()
# marged csv-path list
for (i in 1:length(tmp.list)) {
  mkt.name <- sub(".csv", "", unlist(strsplit(tmp.list[i], "/"))[3])  # ex.TSE1
  tmp.master.SIC[[i]] <- read.csv(tmp.list[i], header = TRUE, stringsAsFactors = FALSE, fileEncoding = "UTF-8-BOM") # stringsAsFactors:カテゴリ変換しません
  print(paste(mkt.name, nrow(tmp.master.SIC[[i]]), ncol(tmp.master.SIC[[i]])))
  tmp.master.SIC[[i]] <- cbind( mkt.name, tmp.master.SIC[[i]] ) # 市場名とくっつける
  master.SIC <- rbind(master.SIC, tmp.master.SIC[[i]][1:6])
}
#[1] "master.SIC 7936 6[mkt.name,日付,コード,銘柄名,市場.商品区分,X33業種コード]"
print(paste('master.SIC', nrow(master.SIC), paste0(ncol(master.SIC), '[', paste(colnames(master.SIC), collapse=","), ']')) )
# 数字から始まる項目名には勝手にXがつくようだ。それを削除している
colnames(master.SIC) <- sub("X","",colnames(master.SIC))
rm(list=c("i", "mkt.name", ls(pattern = "tmp*"))) # cleanup

# Output Securities-Code（master_SIC.txtという名前で中間出力する）
write.table(master.SIC, "./master/master_SIC.txt", sep = "\t", col.names = TRUE, row.names = TRUE, fileEncoding = "UTF-8")

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



# ########################
# ここまで読解終わってます
# ########################

# Get XBRL
for (strSIC in SICs[1:1]){

  Sys.sleep(10)
  
  # Send Request
  strURL <- paste0(api.service.url, "/query/", strSIC) # Concat 'URI' 'Securities-Code'
  Sys.sleep(1)

  # Get res
  req <- httpGET(strURL) 
  
  # Exchange API-Response to XMLInternalDocument from xmlParse
  objXML <- xmlParse(req,encoding="UTF-8")
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