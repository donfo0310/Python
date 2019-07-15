get_add_y = function(i){
    y = 1900 + as.POSIXlt(Sys.Date())$year  # 現在の年
    return (y + i)
}

get_add_ym = function(i){
    y = 1900 + as.POSIXlt(Sys.Date())$year  # 現在の年
    m = as.POSIXlt(Sys.Date())$mon + 1      # 現在の月
    # 加算して12を超えた
    if (m + i > 12) {
        m = (m + i) %%12 # 加算後の12の剰余を取る
        y = y + 1
    }else{
        m = (m + i)
    }
    return (as.integer(paste0(y, formatC(m, width=2, flag="0"))))
}

get_add_y2 = function(yyyy, i){
    y = yyyy  # 任意の年
    return (y + i)
}

get_add_ym2 = function(yyyymm, i){
    y = as.integer(substr(yyyymm, 1, 4))    # 任意の年
    m = as.integer(substr(yyyymm, 5, 6))    # 任意の月
    # 加算して12を超えた
    if (m + i > 12) {
        m = (m + i) %%12 # 加算後の12の剰余を取る
        y = y + 1
    }else{
        m = (m + i)
    }
    return (as.integer(paste0(y, formatC(m, width=2, flag="0"))))
}
