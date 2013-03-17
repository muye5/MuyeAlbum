// Copyright (c) 2013 Future
// Author: Muye (muyepiaozhou@gmail.com)

#include <iostream>
#include <iomanip>
#include <string>
#include <cstdlib>
#include <vector>
#include <dirent.h>
#include <cstddef>
#include <unistd.h>
#include <opencv/cv.h>
#include <opencv/cxcore.h>
#include <opencv/highgui.h>
#include <pHash.h>

using namespace std;
using namespace cv;

struct Finger {
    string name;
    uint64_t finger;
    Finger(const string& s = "", uint64_t f = 0) : name(s), finger(f) {}
    Finger(const Finger& f) : name(f.name), finger(f.finger) {}
};

void FileName(vector<Finger>& v, const string& path) {
    DIR *dir = opendir(path.c_str());
    if(!dir) {
        cerr << "Cann't open path " << path << endl;
        return;
    }
    struct dirent *dir_entry;
    while((dir_entry = readdir(dir)) != 0) {
        if(strcmp(dir_entry->d_name, ".") && strcmp(dir_entry->d_name, "..")) {
            v.push_back(Finger(path + "/" + string(dir_entry->d_name)));
        }
    }
}

void FingerExtract(vector<Finger>& v) {
    IplImage *src = 0;          //源图像指针
    IplImage *dst = 0;          //目标图像指针
    IplImage *gst = 0;          //目标图像指针
    CvSize dst_cvsize;          //目标图像尺寸
    vector<Finger>::iterator it = v.begin();
    for(; it != v.end(); ++it) {
        src = cvLoadImage((it->name).c_str());
        dst_cvsize.width = 8;
        dst_cvsize.height = 8;
        dst = cvCreateImage(dst_cvsize, src->depth, src->nChannels); //构造目标图象
        gst = cvCreateImage(dst_cvsize, src->depth, 1); //构造目标图象
        cvResize(src, dst, CV_INTER_LINEAR); //缩放源图像到目标图像
        cvCvtColor(dst, gst, CV_BGR2GRAY); //转为灰度图
        int step = gst->widthStep;
        unsigned int average = 0;
        int v = 0;
        for(int i = 0; i < dst_cvsize.height; ++i) {
            for(int j = 0; j < dst_cvsize.width; ++j) {
                v = (unsigned char)(gst->imageData)[i*step+j];
                average += v;
            }
        }
        average = average / 64;
        uint64_t finger = 0;
        for(int i = 0; i < dst_cvsize.height; ++i) {
            for(int j = 0; j < dst_cvsize.width; ++j) {
                finger <<= 1;
                finger += ((unsigned)(gst->imageData)[i*step+j] > average);
            }
        }
        it->finger = finger;
        cvReleaseImage(&src);   //释放源图像占用的内存
        cvReleaseImage(&dst);   //释放目标图像占用的内存
        cvReleaseImage(&gst);   //释放目标图像占用的内存
    }
}

void FingerPhash(vector<Finger>& v) {
    vector<Finger>::iterator it = v.begin();
    uint64_t finger;
    for(; it != v.end(); ++it) {
        if(ph_dct_imagehash((it->name).c_str(), finger) < 0) {
            continue;
        }
        it->finger = finger;
    }
}

int main(int argc ,char ** argv) {
    if(argc < 3) {
        cout << "expected: \"./finger image-input-dir image-compare-dir" << endl;
        exit(-1);
    } else {
        vector<Finger> v, u;

        FileName(v, argv[1]);
        FileName(u, argv[2]);

        FingerExtract(v);
        FingerExtract(u);

        cout << "Simple Result:" << endl;
        vector<Finger>::iterator it1 = v.begin();
        vector<Finger>::iterator it2 = u.begin();
        for(;it1 != v.end() && it2 != u.end(); ++it1, ++it2) {
            cout << it1->name << " : ["
               << setw(16) << hex << it1->finger << "] : ["
               << setw(16) << hex << it2->finger << "]" << endl;
            cout << "hamming distance : " << ph_hamming_distance(it1->finger, it2->finger) << endl;
        }
        cout << "======================================================" << endl;

        FingerPhash(v);
        FingerPhash(u);

        cout << "pHash Result:" << endl;
        it1 = v.begin();
        it2 = u.begin();
        for(;it1 != v.end() && it2 != u.end(); ++it1, ++it2) {
            cout << it1->name << " : ["
               << setw(16) << hex << it1->finger << "] : ["
               << setw(16) << hex << it2->finger << "]" << endl;
            cout << "hamming distance : " << ph_hamming_distance(it1->finger, it2->finger) << endl;
        }
    }
    return 0;
}


