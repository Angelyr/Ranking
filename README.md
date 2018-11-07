# Large Scale Programming - Ranking Team Green x

## How to run

Since we use "Simple-Web-Server" as a library for this project, in order to run the code you need cmake and boost installed on your computer. Then follow these steps to build the project:


mkdir build
cd build
cmake ..
make
cd ..

Make sure cmake is using a c++11 compiler (newest g++ should be fine)

When adding files, you may need to add to the CMakeLists.txt file to add an executable

Run the ranking server with: ./build/RankingRestServer

This will serve on localhost:8083

You can send a raw POST request with a string and it will return the content length

 
