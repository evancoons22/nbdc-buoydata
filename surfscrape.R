library(polite)
library(rvest)

get_ht <- function() {
  # Get current date and time
  # print(Sys.time())
  now <- Sys.time()
  year <- format(now, "%Y")
  month <- format(now, "%m")
  day <- format(now, "%d")
  hour <- format(now, "%H")
  minute <- format(now, "%M")

  # Scrape the data
  session <- bow("https://www.surfline.com/surf-report/el-porto/5842041f4e65fad6a7708906?camId=5a203892096c27001ac4f18d") 
  surfpage <- session %>% 
    scrape(content = "text/html; charset=UTF-8")
  waveht <- surfpage %>% html_nodes(".mui-style-qfj0fo") %>% html_text()

  return(waveht)

  # Connect to the SQLite database
  # con <- dbConnect(SQLite(), dbname = "db.db")

  # Insert the data into the database
  # query <- paste("INSERT INTO conditions (year, month, day, hour, minute, ht) VALUES (", 
                 # year, ", ", month, ", ", day, ", ", hour, ", ", minute, ", '", waveht, "')", sep = "")
  # dbExecute(con, query)

  # Close the connection
  # dbDisconnect(con)
}
print(get_ht())

# update_data()

# while(TRUE) {
#   # Get the current time
#   now <- Sys.time()
#   hour <- as.integer(format(now, "%H"))
#   minute <- as.integer(format(now, "%M"))

#   # If it's 6am, 12pm, 6pm, or 12am, run the update function
#   if ((hour == 6 || hour == 12 || hour == 18 || hour == 0) && minute == 0) {
#     update_data()
#   }

#   # Wait for 60 seconds before checking the time again
#   Sys.sleep(60)
# }


