def compress(uncompressed):
  
  text = list(uncompressed)
  search_window = []
  tags = [] # list of dictionaries to hold the 3 values 
  matching_indices = [] # to collect all the matched chars in the search window
  matching_lengths = [] # getting the matching length for each matched char "list of dictionaries to hold each matching index and its length"

  i = 0
  while i < len(text):
  
    x = text[i]

    if len(search_window) == 0 or x not in search_window: # first char / first occurance
      search_window.append(x)
      tags.append({"pos":0, "len":0, "sym":x})
      i += 1 # go to next char/move by 1
      continue

    for j in range(len(search_window) - 1, -1, -1): # looping in the search window from the end
      if x != search_window[j]: 
        continue
      else:
        matching_indices.append(j)
    
    for index in matching_indices: # getting each matched char & calculate the consecutive match length 
      search_index = index
      look_index = i # to loop lookahead buffer characters

      length = 0
      while search_index < len(search_window) and look_index < len(text):
        if search_window[search_index] == text[look_index]:
          length += 1
          search_index += 1
          look_index += 1
        else:
          break
      
      matching_lengths.append({"i":index, "len":length})

    # handling repetitive & overlapping sequence
    for matched in matching_lengths:

      index = matched["i"]
      length = matched["len"]

      if index + length == len(search_window) and length > 0:
        distance = len(search_window) - index
        offset = length

        while i + offset < len(text):
          pattern_index = offset % distance 
          source_index = index + pattern_index
          if text[i + offset] == search_window[source_index]:
            length += 1
            offset += 1
          else:
            break

        matched["len"] = length


    # getting the longest match with the nearest position 
    longest_match = max(matching_lengths, key=lambda matched: (matched["len"], matched["i"]))
    
    # updating the search window
    index_to_add = longest_match["i"]
    for k in range(longest_match["len"]):
      search_window.append(search_window[index_to_add])
      index_to_add += 1

    # adding the symbol after the matched sequence
    if len(search_window) < len(text): # adding the char after finding & adding the match itself if not it's the last char
      search_window.append(text[i + longest_match["len"]])

    # handling the last char properly
    if i + longest_match["len"] < len(text): 
      symbol = text[i + longest_match["len"]]
    else:
      symbol = "NULL"

  
    tags.append({"pos":i-longest_match["i"], "len":longest_match["len"], "sym":symbol})

    # moves to the next char after appending the whole matched block
    i = i + longest_match["len"] + 1 
    matching_indices = []
    matching_lengths = []

        

  for i in range(len(tags)):
    print(f"< {tags[i]["pos"]} , {tags[i]["len"]} , {tags[i]["sym"]} >") # keep it now for debugging

  return tags