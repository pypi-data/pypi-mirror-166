╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                               [1mLecture 0[0m                                                                ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

[1;33m • [0m]8;id=638363;#welcome\[94mWelcome[0m]8;;\                                                                                                                                
[1;33m • [0m]8;id=299509;#what-is-computer-science\[94mWhat is computer science?[0m]8;;\                                                                                                              
[1;33m • [0m]8;id=210564;#representing-numbers\[94mRepresenting numbers[0m]8;;\                                                                                                                   
[1;33m • [0m]8;id=456801;#text\[94mText[0m]8;;\                                                                                                                                   
[1;33m • [0m]8;id=677390;#images-video-sounds\[94mImages, video, sounds[0m]8;;\                                                                                                                  
[1;33m • [0m]8;id=90989;#algorithms\[94mAlgorithms[0m]8;;\                                                                                                                             
[1;33m • [0m]8;id=34572;#pseudocode\[94mPseudocode[0m]8;;\                                                                                                                             
[1;33m • [0m]8;id=838337;#scratch-basics\[94mScratch basics[0m]8;;\                                                                                                                         
[1;33m • [0m]8;id=907429;#abstraction\[94mAbstraction[0m]8;;\                                                                                                                            
[1;33m • [0m]8;id=818921;#conditionals-and-more\[94mConditionals and more[0m]8;;\                                                                                                                  
[1;33m • [0m]8;id=112978;#demos\[94mDemos[0m]8;;\                                                                                                                                  


                                                                 [1;4mWelcome[0m                                                                  

[1;33m • [0mThis year, we’re back in Sanders Theatre, and David took CS50 himself as a sophomore years ago, but only because the professor at the  
[1;33m   [0mtime allowed him to take the course pass/fail.                                                                                         
[1;33m • [0mIt turns out that computer science was less about programming than about problem solving. And though there may be frustration from     
[1;33m   [0mfeeling stuck or making mistakes, there will also be a great sense of gratification and pride from getting something to work or        
[1;33m   [0mcompleting some task.                                                                                                                  
[1;33m • [0mIn fact, David lost two points on his first assignment for not following all of the instructions correctly:                            

🌆 ]8;id=906023;assignment.png\assignment showing code with -2 points]8;;\  + And while this code (written in a programming language as opposed to a language like English)
weeks or months before we can understand main programming concepts and even teach ourselves new languages.                                

[1;33m • [0mImportantly,                                                                                                                           

[35m▌ [0m[35mwhat ultimately matters in this course is not so much where you end up relative to your classmates but where you end up relative to [0m[35m  [0m
[35m▌ [0m[35myourself when you began[0m[35m                                                                                                               [0m

[1;33m • [0mIn fact, two-thirds of CS50 students have never taken a computer science course before.                                                


                                                        [1;4mWhat is computer science?[0m                                                         

[1;33m • [0mComputer science is fundamentally problem solving, but we’ll need to be precise and methodical.                                        
[1;33m • [0mWe can think of [1mproblem solving[0m as the process of taking some input (a problem we want to solve) and generate some output (the solution
[1;33m   [0mto our problem).                                                                                                                       

🌆 ]8;id=562965;input_output.png\word ]8;;\]8;id=562965;input_output.png\"]8;;\]8;id=562965;input_output.png\input]8;;\]8;id=562965;input_output.png\"]8;;\]8;id=562965;input_output.png\, arrow into box, arrow out of box, word ]8;;\]8;id=562965;input_output.png\"]8;;\]8;id=562965;input_output.png\output]8;;\]8;id=562965;input_output.png\"]8;;\                                                                          

[1;33m • [0mTo begin doing that, we’ll need a way to represent inputs and outputs, so we can store and work with information in a standardized way.


                                                           [1;4mRepresenting numbers[0m                                                           

[1;33m • [0mTo count the number of people in a room, we might start by using our fingers, one at a time. This system is called [1munary[0m , where each  
[1;33m   [0mdigit represents a single value of one.                                                                                                
[1;33m • [0mTo count to higher numbers, we might use ten digits, 0 through 9, with a system called [1mdecimal[0m .                                       
[1;33m • [0mComputers use a simpler system called [1mbinary[0m , with just two digits, 0 and 1.                                                          
[1;33m • [0mFor example, in binary this would be 0:                                                                                                

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m0 0 0                                                                                                                                 [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mAnd this would be 1:                                                                                                                   

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m0 0 1                                                                                                                                 [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ (We don’t need the leading zeroes, but we’ll include them to see the patterns more easily.)                                         [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mSince there is no digit for 2, we’ll need to change another digit to represent the next number:                                        

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m0 1 0                                                                                                                                 [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mThen we’ll “add 1” to represent 3:                                                                                                     

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m0 1 1                                                                                                                                 [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mAnd continue the pattern for 4 …:                                                                                                      

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m1 0 0                                                                                                                                 [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0m… 5 …:                                                                                                                                 

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m1 0 1                                                                                                                                 [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0m… 6 …:                                                                                                                                 

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m1 1 0                                                                                                                                 [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0m… and 7:                                                                                                                               

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m1 1 1                                                                                                                                 [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mEach [3mbinary digit[0m is also called a [1mbit[0m .                                                                                               
[1;33m • [0mSince computers run on electricity, which can be turned on or off, we can simply represent a bit by turning some switch on or off to   
[1;33m   [0mrepresent a 0 or 1.                                                                                                                    
[1;33m • [0mInside modern computers, there are billions of tiny switches called [1mtransistors[0m that can be turned on and off to represent different   
[1;33m   [0mvalues.                                                                                                                                
[1;33m • [0mAnd the pattern to count in binary with multiple bits is the same as the pattern in decimal with multiple digits.                      
[1;33m • [0mFor example, we know the following number in decimal represents one hundred and twenty-three.                                          

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m1 2 3                                                                                                                                 [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ The                                                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34m `3`                                                                                                                                  [0m [2m│[0m
[2m│[0m [48;2;39;40;34m is in the ones place, the                                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34m `2`                                                                                                                                  [0m [2m│[0m
[2m│[0m [48;2;39;40;34m is in the tens place, and the                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34m `1`                                                                                                                                  [0m [2m│[0m
[2m│[0m [48;2;39;40;34m is in the hundreds place.                                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34m+ So                                                                                                                                  [0m [2m│[0m
[2m│[0m [48;2;39;40;34m `123`                                                                                                                                [0m [2m│[0m
[2m│[0m [48;2;39;40;34m is                                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34m `100×1 + 10×2 + 1×3 = 100 + 20 + 3 = 123`                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34m .                                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m+ Each place for a digit represents a power of ten, since there are ten possible digits for each place. The rightmost place is for 10 [0m [2m│[0m
[2m│[0m [48;2;39;40;34m 0                                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m , the middle one 10                                                                                                                  [0m [2m│[0m
[2m│[0m [48;2;39;40;34m 1                                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m , and the leftmost place 10                                                                                                          [0m [2m│[0m
[2m│[0m [48;2;39;40;34m 2                                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m :                                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34m```                                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34m102 101 100                                                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34m1   2   3                                                                                                                             [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34m```                                                                                                                                   [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mIn binary, with just two digits, we have powers of two for each place value:                                                           

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m22 21 20                                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m#  #  #                                                                                                                               [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ This is equivalent to:                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34m```                                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34m4  2  1                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m#  #  #                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34m```                                                                                                                                   [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWith all the light bulbs or switches off, we would still have a value of 0:                                                            

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m4 2 1                                                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34m**0 0 0**                                                                                                                             [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mNow if we change the binary value to, say, [97;40m0 1 1[0m , the decimal value would be 3, since we add the 2 and the 1:                         

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m4 2 1                                                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34m**0 1 1**                                                                                                                             [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mTo count higher than 7, we would need another bit to the left to represent the number 8.                                               
[1;33m • [0mMost computers use 8 bits at a time, like [97;40m00000011[0m for the number 3.                                                                   


                                                                   [1;4mText[0m                                                                   

🌆 ]8;id=219804;medical_mask.png\emoji with face with medical mask]8;;\ 
[1;33m • [0mTo represent letters, all we need to do is decide how numbers map to letters. Some humans, many years ago, collectively decided on a   
[1;33m   [0mstandard mapping of numbers to letters. The letter “A”, for example, is the number 65, and “B” is 66, and so on. In binary, the letter 
[1;33m   [0m“A” is the pattern [97;40m01000001[0m . By using context, like the file format, different programs can interpret and display the same bits as    
[1;33m   [0mnumbers or text.                                                                                                                       
[1;33m • [0mThe standard mapping, ]8;id=605029;https://en.wikipedia.org/wiki/ASCII\[1;94mASCII[0m]8;;\ , also includes lowercase letters and punctuation.                                                         
[1;33m • [0mWhen we receive a text message, we might be getting patterns of bits that have the decimal values [97;40m72[0m , [97;40m73[0m , and [97;40m33[0m . Those bits would  
[1;33m   [0mmap to the letters [97;40mHI![0m . And the sequences of bits we receive would look like [97;40m01001000[0m , [97;40m01001001[0m , and [97;40m00100001[0m , with 8 bits for each
[1;33m   [0mcharacter.                                                                                                                             
[1;33m • [0mWith eight bits, or one byte, we can have 2 8 , or 256 different values (including zero). (The highest [3mvalue[0m we can count up to would  
[1;33m   [0mbe 255.)                                                                                                                               
[1;33m • [0mAnd we might already be familiar with using bytes as a unit of measurement for data, as in megabytes or gigabytes, for millions or     
[1;33m   [0mbillions of bytes.                                                                                                                     
[1;33m • [0mOther characters, such as letters with accent marks and symbols in other languages, are part of a standard called ]8;id=568419;https://en.wikipedia.org/wiki/Unicode\[1;94mUnicode[0m]8;;\ , which uses 
[1;33m   [0mmore bits than ASCII to accommodate all these characters.                                                                              
[1;33m • [0mWhen we receive an ]8;id=863292;https://en.wikipedia.org/wiki/Emoji\[94memoji[0m]8;;\ , our computer is actually just receiving a number in binary that it then maps to the image of the emoji based
[1;33m   [0mon the Unicode standard.                                                                                                               
[1;33m   [0m[1;33m • [0mFor example, the “face with medical mask” emoji is just the four bytes [97;40m11110000 10011111 10011000 10110111[0m :                        
[1;33m   [0m                                                                                                                                       
[1;33m   [0m[1;33m • [0mAnd it turns out that different companies that create software for their devices will have slightly different images that represent 
[1;33m   [0m[1;33m   [0meach emoji, since only the descriptions have been standardized.                                                                     


                                                          [1;4mImages, video, sounds[0m                                                           

🌆 ]8;id=210175;72_73_33.png\dark yellow]8;;\ 
[1;33m • [0mWith bits, we can map numbers to colors as well. There are many different systems to represent colors, but a common one is [1mRGB[0m , which 
[1;33m   [0mrepresents colors by indicating the amount of red, green, and blue within each color.                                                  
[1;33m • [0mFor example, our pattern of bits earlier, [97;40m72[0m , [97;40m73[0m , and [97;40m33[0m might indicate the amount of red, green, and blue in a color. (And our      
[1;33m   [0mprograms would know those bits map to a color if we opened an image file, as opposed to receiving them in a text message.)             
[1;33m   [0m[1;33m • [0mEach number might be 8 bits, with 256 possible values, so with three bytes, or 24 bits, we can represent millions of colors. Our    
[1;33m   [0m[1;33m   [0mthree bytes from above would represent a dark shade of yellow:                                                                      
[1;33m   [0m                                                                                                                                       
[1;33m • [0mThe dots, or squares, on our screens are called [1mpixels[0m , and images are made up of many thousands or millions of those pixels as well. 
[1;33m   [0mSo by using three bytes to represent the color for each pixel, we can create images. We can see pixels in an emoji if we zoom in, for  
[1;33m   [0mexample:                                                                                                                               

🌆 ]8;id=718994;emoji_zoomed.png\zoomed-in emoji of face with medical mask with squares of pixels distinguishable]8;;\                                                       

[1;33m • [0mVideos are sequences of many images, changing multiple times a second to give us the appearance of motion, as a ]8;id=989896;https://www.youtube.com/watch?v=sz78_07Xg-U\[94mflipbook[0m]8;;\ might.        
[1;33m • [0mMusic can be represented with bits, too. ]8;id=244872;https://en.wikipedia.org/wiki/MIDI\[94mMIDI[0m]8;;\ is one such format which represents music with numbers for each of the notes and their   
[1;33m   [0mduration and volume.                                                                                                                   
[1;33m • [0mSo all of these ideas are just zeroes and ones, interpreted and used by software we’ve written to interpret them in the ways that we   
[1;33m   [0mwant.                                                                                                                                  
[1;33m   [0m[1;33m • [0mThere are other formats, some of which use compression (mathematical ways to represent some data with fewer bits), or some which    
[1;33m   [0m[1;33m   [0mmight be containers that store multiple types of data together.                                                                     
[1;33m   [0m[1;33m • [0mAnd since there are many companies and groups developing software, we have lots of different file formats in existence, each with   
[1;33m   [0m[1;33m   [0mtheir own ways of representing data. But there are also organizations that work on some consensus, like ]8;id=984889;https://en.wikipedia.org/wiki/Unicode_Consortium\[94mthe one[0m]8;;\ responsible for     
[1;33m   [0m[1;33m   [0mmaintaining the Unicode standard.                                                                                                   


                                                                [1;4mAlgorithms[0m                                                                

[1;33m • [0mNow that we can represent inputs and outputs, we can work on problem solving. The black box that transforms inputs to outputs contains 
[1;33m   [0m[1malgorithms[0m , step-by-step instructions for solving problems:                                                                           

🌆 ]8;id=526515;algorithms.png\box with word ]8;;\]8;id=526515;algorithms.png\"]8;;\]8;id=526515;algorithms.png\algorithms]8;;\]8;id=526515;algorithms.png\"]8;;\                                                                                                             

[1;33m • [0mWe might have an application on our phones that store our contacts, with their names and phone numbers sorted alphabetically. The      
[1;33m   [0mold-school equivalent might be a phone book, a printed copy of names and phone numbers.                                                
[1;33m • [0mWe might open the book and start from the first page, looking for a name one page at a time. This algorithm would be correct, since we 
[1;33m   [0mwill eventually find the name if it’s in the book.                                                                                     
[1;33m • [0mWe might flip through the book two pages at a time, but this algorithm will not be correct since we might skip the page with our name  
[1;33m   [0mon it.                                                                                                                                 
[1;33m • [0mAnother algorithm would be opening the phone book to the middle, decide whether our name will be in the left half or right half of the 
[1;33m   [0mbook (because the book is alphabetized), and reduce the size of our problem by half. We can repeat this until we find our name,        
[1;33m   [0mdividing the problem in half each time.                                                                                                
[1;33m • [0mWe can visualize the efficiency of each of those algorithms with a chart:                                                              

🌆 ]8;id=969970;time_to_solve.png\chart with: ]8;;\]8;id=969970;time_to_solve.png\"]8;;\]8;id=969970;time_to_solve.png\size of problem]8;;\]8;id=969970;time_to_solve.png\"]8;;\]8;id=969970;time_to_solve.png\ as x-axis; ]8;;\]8;id=969970;time_to_solve.png\"]8;;\]8;id=969970;time_to_solve.png\time to solve]8;;\]8;id=969970;time_to_solve.png\"]8;;\]8;id=969970;time_to_solve.png\ as y-axis; red, steep straight line from origin to top of graph labeled ]8;;\]8;id=969970;time_to_solve.png\"]8;;\]8;id=969970;time_to_solve.png\n]8;;\]8;id=969970;time_to_solve.png\"]8;;\]8;id=969970;time_to_solve.png\; ]8;;\
]8;id=969970;time_to_solve.png\yellow, less steep straight line from origin to top of graph labeled ]8;;\]8;id=969970;time_to_solve.png\"]8;;\]8;id=969970;time_to_solve.png\n/2]8;;\]8;id=969970;time_to_solve.png\"]8;;\]8;id=969970;time_to_solve.png\; green, curved line that gets less and less steep from origin ]8;;\
]8;id=969970;time_to_solve.png\to right of graph labeled ]8;;\]8;id=969970;time_to_solve.png\"]8;;\]8;id=969970;time_to_solve.png\log]8;;\]8;id=969970;time_to_solve.png\_]8;;\]8;id=969970;time_to_solve.png\2  n]8;;\]8;id=969970;time_to_solve.png\"]8;;\  + Our first algorithm, searching one page at a time, can be represented by the red line: our time to
of the problem increases. [3mn[0m is a number representing the size of the problem, so with [3mn[0m pages in our phone books, we have to take up to [3mn[0m 
steps to find a name. + The second algorithm, searching two pages at a time, can be represented by the yellow line: our slope is less     
steep, but still linear. Now, we only need (roughly) [3mn[0m / 2 steps, since we flip two pages at a time. + Our final algorithm, dividing the  
phone book in half each time, can be represented by the green line, with a fundamentally different relationship between the size of the   
problem and the time to solve it. If the phone book doubled in size from 1000 to 2000 pages, we would only need one more step to find our 
name.                                                                                                                                     


                                                                [1;4mPseudocode[0m                                                                

[1;33m • [0mWe can write [1mpseudocode[0m , which is a representation of our algorithm in precise English (or some other human language):                

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m1  Pick up phone book                                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34m2  Open to middle of phone book                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m3  Look at page                                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m4  If person is on page                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m5      Call person                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m6  Else if person is earlier in book                                                                                                  [0m [2m│[0m
[2m│[0m [48;2;39;40;34m7      Open to middle of left half of book                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34m8      Go back to line 3                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m9  Else if person is later in book                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m10     Open to middle of right half of book                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34m11     Go back to line 3                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m12 Else                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m13     Quit                                                                                                                           [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ With these steps, we check the middle page, decide what to do, and repeat. If the person isn’t on the page, and there’s no more     [0m [2m│[0m
[2m│[0m [48;2;39;40;34mpages in the book left, then we stop. And that final case is particularly important to remember. When programs or code don’t include  [0m [2m│[0m
[2m│[0m [48;2;39;40;34mthat final case, they might appear to freeze or stop responding, or continue to repeat the same work over and over without making any [0m [2m│[0m
[2m│[0m [48;2;39;40;34mprogress.                                                                                                                             [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mSome of these lines start with actions or verbs that solve a smaller problem. We’ll start calling these [3mfunctions[0m :                    

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m1  **Pick up** phone book                                                                                                             [0m [2m│[0m
[2m│[0m [48;2;39;40;34m2  **Open to** middle of phone book                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34m3  **Look at** page                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34m4  If person is on page                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m5      **Call** person                                                                                                                [0m [2m│[0m
[2m│[0m [48;2;39;40;34m6  Else if person is earlier in book                                                                                                  [0m [2m│[0m
[2m│[0m [48;2;39;40;34m7      **Open to** middle of left half of book                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34m8      Go back to line 3                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m9  Else if person is later in book                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m10     **Open to** middle of right half of book                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m11     Go back to line 3                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m12 Else                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m13     **Quit**                                                                                                                       [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe also have branches that lead to different paths, like forks in the road, which we’ll call [3mconditionals[0m :                            

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m1  Pick up phone book                                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34m2  Open to middle of phone book                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m3  Look at page                                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m4  **If** person is on page                                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34m5      Call person                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m6  **Else if** person is earlier in book                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m7      Open to middle of left half of book                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34m8      Go back to line 3                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m9  **Else if** person is later in book                                                                                                [0m [2m│[0m
[2m│[0m [48;2;39;40;34m10     Open to middle of right half of book                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34m11     Go back to line 3                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m12 **Else**                                                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34m13     Quit                                                                                                                           [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mAnd the questions that decide where we go are called [3mBoolean expressions[0m , which eventually result in answers of yes or no, or true or 
[1;33m   [0mfalse:                                                                                                                                 

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m1  Pick up phone book                                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34m2  Open to middle of phone book                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m3  Look at page                                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m4  If **person is on page**                                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34m5      Call person                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m6  Else if **person is earlier in book**                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m7      Open to middle of left half of book                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34m8      Go back to line 3                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m9  Else if **person is later in book**                                                                                                [0m [2m│[0m
[2m│[0m [48;2;39;40;34m10     Open to middle of right half of book                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34m11     Go back to line 3                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m12 Else                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m13     Quit                                                                                                                           [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mLastly, we have words that create cycles, where we can repeat parts of our program, called [3mloops[0m :                                     

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m1  Pick up phone book                                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34m2  Open to middle of phone book                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m3  Look at page                                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m4  If person is on page                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m5      Call person                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m6  Else if person is earlier in book                                                                                                  [0m [2m│[0m
[2m│[0m [48;2;39;40;34m7      Open to middle of left half of book                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34m8      **Go back to line 3**                                                                                                          [0m [2m│[0m
[2m│[0m [48;2;39;40;34m9  Else if person is later in book                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m10     Open to middle of right half of book                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34m11     **Go back to line 3**                                                                                                          [0m [2m│[0m
[2m│[0m [48;2;39;40;34m12 Else                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m13     Quit                                                                                                                           [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe’ll soon encounter other ideas, too:                                                                                                 
[1;33m   [0m[1;33m • [0mfunctions                                                                                                                           
[1;33m   [0m[1;33m   [0m[1;33m • [0marguments, return values                                                                                                         
[1;33m   [0m[1;33m • [0mconditionals                                                                                                                        
[1;33m   [0m[1;33m • [0mBoolean expressions                                                                                                                 
[1;33m   [0m[1;33m • [0mloops                                                                                                                               
[1;33m   [0m[1;33m • [0mvariables                                                                                                                           
[1;33m   [0m[1;33m • [0m…                                                                                                                                   
[1;33m • [0mAnd David’s first program just printed “hello, world” to the screen:                                                                   

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m#include <stdio.h>                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mint main(void)                                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34m{                                                                                                                                     [0m [2m│[0m
[2m│[0m [48;2;39;40;34m    printf("hello, world\n");                                                                                                         [0m [2m│[0m
[2m│[0m [48;2;39;40;34m}                                                                                                                                     [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ But this program, written in a language called C, has lots of other syntax that keeps us from focusing on these core ideas.         [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m


                                                              [1;4mScratch basics[0m                                                              

[1;33m • [0mWe’ll start programming with a graphical programming language called ]8;id=628325;https://scratch.mit.edu/\[94mScratch[0m]8;;\ , where we’ll drag and drop blocks that contain           
[1;33m   [0minstructions.                                                                                                                          
[1;33m • [0mThe programming environment for Scratch is a little more friendly:                                                                     

🌆 ]8;id=942634;scratch.png\screenshot of Scratch]8;;\]8;id=942634;scratch.png\']8;;\]8;id=942634;scratch.png\s interface]8;;\  + On the left, we have puzzle pieces that represent functions or variables, or other concepts, that 
area in the center. + On the bottom right, we can add more characters, or sprites, for our program to use. + On the top right, we have a  
stage, or the world that will be shown by our program.                                                                                    

[1;33m • [0mThe world in Scratch has a coordinate-based system for positioning things on the screen:                                               

🌆 ]8;id=372963;coordinates.png\cat in center of screen with x and y axes labeled with negative and positive coordinates]8;;\  + The center of the screen is a coordinate of
the screen would still be 0 for x, and -180 for y. The left of the screen would be -240 for x and 0 for y, and the right of the screen    
would be 240 for x and 0 for y.                                                                                                           

[1;33m • [0mScratch also categorizes its pieces, each of which might be a function, conditional, or more:                                          
[1;33m   [0m[1;33m • [0mThe “Motion” category has functions like the “move” block that will do something:                                                   
[1;33m   [0m[2m┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[1;33m   [0m[2m│[0m [48;2;39;40;34mmove () steps                                                                                                                      [0m [2m│[0m
[1;33m   [0m[2m└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m
[1;33m   [0m[1;33m • [0mIn the “Events” category, we can see blocks that will activate when something happens, like when the green flag on top of the stage 
[1;33m   [0m[1;33m   [0mis clicked:                                                                                                                         
[1;33m   [0m[2m┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[1;33m   [0m[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                            [0m [2m│[0m
[1;33m   [0m[2m└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m
[1;33m   [0m[1;33m • [0m“Control” has conditionals, each of which will only do something if the Boolean expression inside is true:                          
[1;33m   [0m[2m┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[1;33m   [0m[2m│[0m [48;2;39;40;34mif <> then                                                                                                                         [0m [2m│[0m
[1;33m   [0m[2m└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m
[1;33m   [0m[1;33m • [0m“Sensing” includes those Boolean expressions, or questions like whether the sprite is touching the mouse pointer:                   
[1;33m   [0m[2m┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[1;33m   [0m[2m│[0m [48;2;39;40;34m<touching (mouse-pointer v) ?>                                                                                                     [0m [2m│[0m
[1;33m   [0m[2m└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m
[1;33m   [0m[1;33m • [0m“Operators” contains blocks that let us do math or pick random numbers, or combine multiple Boolean expressions:                    
[1;33m   [0m[2m┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[1;33m   [0m[2m│[0m [48;2;39;40;34m<> and <>                                                                                                                          [0m [2m│[0m
[1;33m   [0m[2m└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m
[1;33m   [0m[1;33m • [0m“Variables” will let us store values like words or numbers, and save them with names like [97;40mx[0m , [97;40my[0m , or other full words to describe   
[1;33m   [0m[1;33m   [0mthem.                                                                                                                               
[1;33m   [0m[1;33m • [0mWe can even combine multiple blocks ourselves into a new puzzle piece, or function, with “My Blocks”.                               
[1;33m • [0mWe can drag a few blocks to make our cat say “hello, world”:                                                                           

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34msay [hello, world]                                                                                                                    [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ The purple block, “say”, is a function that takes some sort of                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34m *input*                                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m , the text in the white oval, and makes our cat say it on the stage as its output.                                                   [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe can also drag in the “ask and wait” block, with a question like “What’s your name?”, and combine it with a “say” block for the      
[1;33m   [0manswer:                                                                                                                                

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mask [What's your name?] and wait                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34msay [hello,]                                                                                                                          [0m [2m│[0m
[2m│[0m [48;2;39;40;34msay (answer)                                                                                                                          [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ The “answer” block is a variable, or value, that stores what the program’s user types in, and we can place it in a “say” block by   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mdraggind and dropping as well.                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34m+ The “ask and wait” block takes in a question as its input (or                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m *argument*                                                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34m ), and stores its                                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34m *return value*                                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34m into the “answer” block as output.                                                                                                   [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mBut we didn’t wait after we said “Hello” with the first block, so we didn’t see the first message of “hello” before it was covered by  
[1;33m   [0mour name. We can use the “join” block to combine two phrases so our cat can say “hello, David”:                                        

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mask [What's your name?] and wait                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34msay (join [hello,] (answer))                                                                                                          [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ Note that the “join” block takes not just one, but two arguments, or inputs, and its                                                [0m [2m│[0m
[2m│[0m [48;2;39;40;34m *output*                                                                                                                             [0m [2m│[0m
[2m│[0m [48;2;39;40;34m , or the combined phrase, is used immediately as the                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34m *input*                                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34m to another function, the “say” block:                                                                                                [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34m![hello, answer blocks as inputs to join block, then output of hello, David as input to say block, then output of cat with speech     [0m [2m│[0m
[2m│[0m [48;2;39;40;34mbubble](join_say.png)                                                                                                                 [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mAt the bottom left of the screen, we see an icon for extensions, and one of them is called Text to Speech. After we add it, we can use 
[1;33m   [0mthe “speak” block to hear our cat speak:                                                                                               

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mask [What's your name?] and wait                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mspeak (join [hello,] (answer))                                                                                                        [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ The Text to Speech extension, thanks to the cloud, or computer servers on the internet, is converting our text to audio.            [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m


                                                               [1;4mAbstraction[0m                                                                

[1;33m • [0mWe can try to make the cat say meow:                                                                                                   

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mplay sound (Meow v) until done                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34mwait (1) seconds                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mplay sound (Meow v) until done                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34mwait (1) seconds                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mplay sound (Meow v) until done                                                                                                        [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ We can have it say meow three times, but now we’re repeating blocks over and over.                                                  [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mLet’s use a loop, or a “repeat” block:                                                                                                 

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mrepeat (3)                                                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34mplay sound (Meow v) until done                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34mwait (1) seconds                                                                                                                      [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ Now our program achieves the same results, but with fewer blocks. We can consider it to have a better design: if there’s something  [0m [2m│[0m
[2m│[0m [48;2;39;40;34mwe wanted to change, we would only need to change it in one place instead of three.                                                   [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe can use the idea of [1mabstraction[0m , or combining several ideas (or puzzle pieces) into one, so we can use and think about them more   
[1;33m   [0measily. We’ll go into the “My Blocks” category, and click “Make a Block”, and call it “meow”:                                          

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mdefine meow                                                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34mplay sound (Meow v) until done                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34mwait (1) seconds                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mrepeat (3)                                                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34mmeow                                                                                                                                  [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ Now, our main set of blocks can just use the custom “meow” block, and we’ll be able to read this code later and understand what it  [0m [2m│[0m
[2m│[0m [48;2;39;40;34mdoes more easily.                                                                                                                     [0m [2m│[0m
[2m│[0m [48;2;39;40;34m+ We could even drag the set of blocks with “define meow” to the bottom of the screen so it’s not visible, and this will still work,  [0m [2m│[0m
[2m│[0m [48;2;39;40;34meven if we don’t know the                                                                                                             [0m [2m│[0m
[2m│[0m [48;2;39;40;34m **implementation details**                                                                                                           [0m [2m│[0m
[2m│[0m [48;2;39;40;34m , or exactly how our custom block works.                                                                                             [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe can change the “meow” block to take an input, so it can repeat any number of times:                                                 

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mdefine meow [n] times                                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34mrepeat (n)                                                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34mplay sound (Meow v) until done                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34mwait (1) seconds                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mmeow [3] times                                                                                                                        [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ Now, our “meow” block achieves the same effect, but we can easily reuse it or change the number of times our cat says meow.         [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mA good strategy when programming is breaking down a larger problem into smaller subproblems, and solving those first.                  


                                                          [1;4mConditionals and more[0m                                                           

[1;33m • [0mWe’ll try to have our cat make a sound if we “pet” it with our mouse:                                                                  

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <touching (mouse-pointer v)?> then                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34mplay sound (Meow v) until done                                                                                                        [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ But this doesn’t seem to work. That’s because the cat is checking whether the mouse pointer is touching it right as the green flag  [0m [2m│[0m
[2m│[0m [48;2;39;40;34mis clicked, and nothing happens since we’re clicking the flag.                                                                        [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe can have our cat check over and over with the “forever” block:                                                                      

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mforever                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <touching (mouse-pointer v)?> then                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34mplay sound (Meow v) until done                                                                                                        [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe can add another extension, “Video Sensing”:                                                                                         

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen video motion > (50)                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34mplay sound (Meow v) until done                                                                                                        [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ Now, if we move in view of the camera slowly, our cat won’t make a sound, but if we move quickly, it will.                          [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m


                                                                  [1;4mDemos[0m                                                                   

[1;33m • [0mWith a volunteer from the audience, we demonstrate a ]8;id=904619;https://scratch.mit.edu/projects/565362715\[94mwhack-a-mole[0m]8;;\ game.                                                                
[1;33m • [0mWe also take a look at ]8;id=733821;https://scratch.mit.edu/projects/277537196\[94mOscartime[0m]8;;\ , another game where the player drags trash into a trashcan for points.                               
[1;33m • [0mWe’ll take a look at how we might have built this program. First, we can add an image of the ]8;id=542097;https://scratch.mit.edu/projects/565133620\[94mlamp post[0m]8;;\ as a backdrop:                  

🌆 ]8;id=580762;lamppost.png\image of lamppost in Scratch]8;;\]8;id=580762;lamppost.png\']8;;\]8;id=580762;lamppost.png\s editor interface]8;;\                                                                                        

[1;33m • [0mThen, we’ll add images of ]8;id=532907;https://scratch.mit.edu/projects/565100517\[94mtrash cans[0m]8;;\ , with one open and one closed:                                                                   

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mswitch costume to (oscar1 v)                                                                                                          [0m [2m│[0m
[2m│[0m [48;2;39;40;34mforever                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <touching (mouse-pointer v)?> then                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34mswitch costume to (oscar2 v)                                                                                                          [0m [2m│[0m
[2m│[0m [48;2;39;40;34melse                                                                                                                                  [0m [2m│[0m
[2m│[0m [48;2;39;40;34mswitch costume to (oscar1 v)                                                                                                          [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ We name these costumes “oscar1” and “oscar2”, and whenever the mouse is touching it, the trash can will appear to be open.          [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mThen, we’ll work on a piece of ]8;id=685363;https://scratch.mit.edu/projects/565117390\[94mfalling trash[0m]8;;\ :                                                                                         

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mgo to x: (pick random (-240) to (240)) y: (180)                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34mforever                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <(distance to (floor v)) > (0)> then                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mchange y by (-3)                                                                                                                      [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ We move the trash sprite to a random horizontal position, and have it move downwards over and over while the distance to the floor  [0m [2m│[0m
[2m│[0m [48;2;39;40;34m(another sprite that’s a black line) is more than 0.                                                                                  [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe’ll allow ]8;id=731950;https://scratch.mit.edu/projects/565119737\[94mdragging trash[0m]8;;\ with these blocks:                                                                                          

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mforever                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <<mouse down?> and <touching (mouse-pointer v) ?>> then                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34mgo to (mouse-pointer v)                                                                                                               [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ If the mouse is down and touching the trash, then our trash will move to the mouse’s location.                                      [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mFinally, we’ll use ]8;id=699803;https://scratch.mit.edu/projects/565472267\[94mvariables[0m]8;;\ to keep track of our score:                                                                               

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mforever                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <touching (Oscar v) ?> then                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34mchange (score) by (1)                                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34mgo to x: (pick random (-240) to (240)) y: (180)                                                                                       [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ Now, we have another sprite called “Oscar”, and if the trash is touching it, then it will add 1 to the “score” variable, and move   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mback to the top at a random horizontal position so we can continue the game.                                                          [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mNow, we’ll take a look at ]8;id=828401;https://scratch.mit.edu/projects/565121265\[94mmoving[0m]8;;\ . Here, we have a few different scripts, one checking for whether keys are being pressed, and one for 
[1;33m   [0mwhether our sprite is touching a wall:                                                                                                 

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mgo to x: (0) y: (0)                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mforever                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mlisten for keyboard                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mfeel for walls                                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mdefine listen for keyboard                                                                                                            [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <key (up arrow v) pressed?> then                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mchange y by (1)                                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34mend                                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <key (down arrow v) pressed?> then                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34mchange y by (-1)                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mend                                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <key (right arrow v) pressed?> then                                                                                                [0m [2m│[0m
[2m│[0m [48;2;39;40;34mchange x by (1)                                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34mend                                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <key (left arrow v) pressed?> then                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34mchange x by (-1)                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mend                                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34m                                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mdefine feel for walls                                                                                                                 [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <touching (left wall v) ?> then                                                                                                    [0m [2m│[0m
[2m│[0m [48;2;39;40;34mchange x by (1)                                                                                                                       [0m [2m│[0m
[2m│[0m [48;2;39;40;34mend                                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <touching (right wall v) ?> then                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mchange x by (-1)                                                                                                                      [0m [2m│[0m
[2m│[0m [48;2;39;40;34mend                                                                                                                                   [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ Our main script, when the green flag is clicked, will move our sprite to the center of the stage at 0, 0 and then “listen for       [0m [2m│[0m
[2m│[0m [48;2;39;40;34mkeyboard” and “feel for walls” forever.                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m+ The custom “listen for keyboard” script has blocks that will change our sprite’s x- or y-coordinate on the stage for each of the    [0m [2m│[0m
[2m│[0m [48;2;39;40;34marrow keys, moving it around.                                                                                                         [0m [2m│[0m
[2m│[0m [48;2;39;40;34m+ The “feel for walls” script will check whether the sprite is now touching a wall, and move it back if it is.                        [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe can make another sprite ]8;id=590175;https://scratch.mit.edu/projects/565127193\[94mbounce[0m]8;;\ back and forth, like it’s getting in our way:                                                        

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mgo to x: (0) y: (0)                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mpoint in direction (90)                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mforever                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mif <<touching (left wall v)?> or <touching (right wall v)?>> then                                                                     [0m [2m│[0m
[2m│[0m [48;2;39;40;34mturn right (180) degrees                                                                                                              [0m [2m│[0m
[2m│[0m [48;2;39;40;34mend                                                                                                                                   [0m [2m│[0m
[2m│[0m [48;2;39;40;34mmove (1) steps                                                                                                                        [0m [2m│[0m
[2m│[0m [48;2;39;40;34mend                                                                                                                                   [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ First, we’ll move the sprite to the middle and have it point 90 degrees to the right.                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m+ Then, we’ll constantly check if it’s touching a wall and turn 180 degrees (reversing direction) if so, and move 1 step every time.  [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe can have one sprite ]8;id=393705;https://scratch.mit.edu/projects/565479840\[94mfollow[0m]8;;\ another:                                                                                                 

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34mwhen green flag clicked                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mgo to (random position v)                                                                                                             [0m [2m│[0m
[2m│[0m [48;2;39;40;34mforever                                                                                                                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34mpoint towards (Harvard v)                                                                                                             [0m [2m│[0m
[2m│[0m [48;2;39;40;34mmove (1) steps                                                                                                                        [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[2m┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐[0m
[2m│[0m [48;2;39;40;34m+ Our sprite will start at a random position, and move towards our “Harvard” sprite one step at a time.                               [0m [2m│[0m
[2m│[0m [48;2;39;40;34m+ We can change the script to move two steps at a time, so it will always catch up.                                                   [0m [2m│[0m
[2m└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘[0m

[1;33m • [0mWe’ll finish by trying out the full ]8;id=322254;https://scratch.mit.edu/projects/565742837\[94mIvy’s Hardest Game[0m]8;;\ with a volunteer.                                                               
[1;33m • [0mSee you next time!                                                                                                                     
