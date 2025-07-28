#include <iostream>
#include <fstream>
#include <sstream>
#include <random>
#include <iomanip>
#include <cmath>
#include <ctime>
#include <algorithm>
#include <uni10.hpp>
#include "../MPO/mpo.h"
#include "../tSDRG_tools/tSDRG_tools.h"
#include "../tSDRG_tools/measure.h"
#include <vector>
#include <string>
#include <utility>
#include <unordered_map>

using namespace std;

group_path = "/ceph/work/NTHU-qubit/LYT/tSDRG_random/tSDRG/Main_15";


void createPath(paralist& para, datalist& data)
{
    std::unordered_map<std::string, std::string> path;
    std::string file_name = para.L + "_P" + para.Pdis + "_m" + para.chi + "_" + para.sample;
    std::string base_path = group_path + "/data_random/" + para.BC + "/" + para.J + "/" + para.D + "/" + para.L + "/" + file_name + "/";

    path["ZL"] = base_path + file_name + "_ZL.txt";
    path["string"] = base_path + file_name + "_string.txt";
    path["corr1"] = base_path + file_name + "_corr1.txt";
    path["corr2"] = base_path + file_name + "_corr2.txt";
    path["w_loc"] = base_path + file_name + "_w_loc.txt";
    path["energy"] = base_path + file_name + "_energy.txt";
    path["J_list"] = base_path + file_name + "_J_list.txt";
    path["seed"] = base_path + file_name + "_seed.txt";

}

bool seedcheck(paralist& para, datalist& data)
{
    path = group_path + "/data_random" + "/" + para.BC + "/"

    return 
}

void parameterRead(string filename, vector<pair<string, string>>& parameter) {
    ifstream file(filename);
    if (!file) {
        cerr << "無法開啟檔案: " << filename << endl;
        return;
    }

    string line;
    while (getline(file, line)) { // 逐行讀取
        // cout << "讀取到: " << line << endl; // 除錯用，確認讀取內容

        istringstream iss(line);
        string key, value_str;

        if (getline(iss, key, ':') && getline(iss, value_str)) {
            // cout << "解析後: " << key << " -> " << value_str << endl; // 確認解析是否成功
            parameter.push_back(make_pair(key, value_str));
        }
    }

    file.close();
}

struct paralist {
    double spin;
    double J;
    string Jstr = to_string(round(J,2))
    Jstr = "Jdis" + Jstr.erase(std::remove(Jstr.begin(), Jstr.end(), '.'), Jstr.end());
    double D;
    string Dstr = to_string(round(D,2))
    Dstr = "Dim" + Dstr.erase(std::remove(Dstr.begin(), Dstr.end(), '.'), Dstr.end());
    int L;
    string Lstr = "L" + to_string(round(L,2))
    int Pdis;
    string BC;
    int chi;
    int sample;
    string check;
    vector<double> J_list;
    double dimerization;
};

struct datalist {
    double ZL;
    double ZLI;
    double ZLC;
    double SOP;
    long long seed;
    string w_loc;
    string corr1;
    string corr2;
    vector<double> J_list;
    vector<double> energy;
    string  message;
};

double sum(vector<double> &J_list, int oddness)
{
    double sum = 0;
    int L = J_list.size();
    for (int i = 0; i < L; i++)
    {
        if(i%2==oddness)
            sum += J_list[i];
    }

    return sum;
}

void Jlist(paralist& para, datalist& data)
{
    random_device rd;             // non-deterministic generator.
    long long seed = rd();
    // long long seed = para.sample;
    data.seed = seed;
    mt19937 genRandom(seed);    // use mersenne twister and seed is rd.
    // mt19937 genFixed(Jseed);     // use mersenne twister and seed is fixed!

    uniform_real_distribution<double> uniform_dis(nextafter(0.0, 1.0), 1.0); // probability distribution of J rand(0^+ ~ 1)

    normal_distribution<double> normal_dis(0,1.0); 
    // if(Pdis==10)
    //     cout << "J_i=(1+d*(-1)^i)eta_i^R" << endl;
    // if(Pdis==20)
    //     cout << "J_i=(1+d*(-1)^i)exp(eta_i*R)" << endl;
    if(para.BC == "PBC")
    {
        for(int i=0; i<para.L; i++)
        {
            double jvar;
            if(para.Pdis==10)
                jvar = uniform_dis(genRandom);
            if(para.Pdis==20)
                jvar = normal_dis(genRandom);
            // double jvar = normal_dis(genRandom);
            jvar = (1 + para.D * pow(-1,i+1)) * Distribution_Random_Variable(para.Pdis, jvar, para.J);
            // cout << jvar << "\n";
            para.J_list[i] = jvar;
        }
    }
    else
    {
        for(int i=0; i<para.L-1; i++)
        {
            double jvar;
            if(para.Pdis==10)
                jvar = uniform_dis(genRandom);
            if(para.Pdis==20)
                jvar = normal_dis(genRandom);
            // double jvar = normal_dis(genRandom);
            jvar = (1 + para.D * pow(-1,i+1)) * Distribution_Random_Variable(para.Pdis, jvar, para.J);
            // cout << jvar << "\n";
            para.J_list[i] = jvar;
        }
    }
}

void parameterSet(paralist& plist, vector<pair<string, string>> parameter)
{

    int L;                      // system size
    int chi;                    // keep state of isometry
    string BC;                  // boundary condition
    int Pdis;                   // model of random variable disturbution
    double Jdis;                // J-coupling disorder strength
    double Dim;			        // Dimerization constant

    for(int i = 0; i<parameter.size(); i++)
    {
        string para = parameter[i].first;
        string value = parameter[i].second;
        // cout << parameter[i].first << endl;
        // cout << para << endl;
        // cout << value << endl;

        if(para=="L")
        {
            L = stoi(value);
            plist.L = L;
            // std::cout << "L:"  << plist.L << std::endl;
        }
        else if(para == "J")
        {
            Jdis = stod(value);
            plist.J = Jdis;
            // std::cout << "Jdis:" << plist.J << std::endl;
        }
        else if(para == "D")
        {
            Dim = stod(value);
            plist.D = Dim;
            // std::cout << "Dim:" << plist.D << std::endl;
        }
        else if(para == "BC")
        {
            BC = value;
            plist.BC = BC;
            // std::cout << "BC:" << plist.BC << std::endl;
        }
        else if(para == "Pdis")
        {
            Pdis = stoi(value);
            plist.Pdis = Pdis;
            // std::cout << "Pdis:" << plist.Pdis << std::endl;
        }
        else if(para == "chi")
        {
            chi = stoi(value);
            plist.chi = chi;
            // std::cout<< "chi:" << plist.chi << std::endl;
        }
                // default:
                // std::cout << "Invalid day" << std::endl;
    }

}


double dimer(double odd, double even)
{
    double dimer = (abs(even) - abs(odd)) /(abs(even) + abs(odd));
    return dimer;
}

void tSDRG_XXZ(paralist& para, datalist& data)
{
    int sample = para.sample;  
    int L = para.L;                      // system size
    int chi = para.chi;                    // keep state of isometry
    string BC = para.BC;                  // boundary condition
    int Pdis = para.Pdis;                   // model of random variable disturbution
    double J = para.J;                // J-coupling disorder strength
    double D = para.D; 			        // Dimerization constant
    double S = para.spin;        // spin dimension
    data.message = "\n------------------------------sample:" + to_string(sample) +"------------------------------\n";
    data.message += "J:" + to_string(J) + "\nD:" + to_string(D) + + "\nL:" + to_string(L) + "\nPdis:" + to_string(Pdis);
    data.message += "\nBC:" + BC  + "\nchi:" + to_string(chi) + "\nsample::" +  to_string(sample) + "\n";

    // mt19937 genRandom(seed);    // use mersenne twister and seed is rd.
    // mt19937 genFixed(seed);     // use mersenne twister and seed is fixed!
    if(BC == "PBC")
    {
        for(int i = 0; i<L;i++)
        {
            para.J_list.push_back(0);
        }
    }
    else
    {
        for(int i = 0; i<L-1;i++)
        {
            para.J_list.push_back(0);
        }
    }
    double s_tempt;
    // do
    // {
    Jlist(para,data);
    

    s_tempt = abs(abs(sum(para.J_list,0)) - abs(sum(para.J_list,1)))/(abs(sum(para.J_list,0)) + abs(sum(para.J_list,1)));
    long long seed = data.seed;    
    para.dimerization = s_tempt;
    data.message += ("\nd_ratio:" + to_string(s_tempt) + "\n");
    // cout << data.message;
    // cout << "d_ratio:" << abs(abs(sum(data.J_list,0)) - abs(sum(data.J_list,1)))/(abs(sum(data.J_list,0)) + abs(sum(data.J_list,1))) <<endl;
    // }
    // while ( s_tempt > error ) ;
    // data.message = data.message;
    // for(int i=0;i<L;i++)
    //     cout << data.J_list[i] << ", ";
    data.message += (to_string(sum(para.J_list,0)) + "\n" + to_string(sum(para.J_list,1)) + "\n");
    // cout << data.message;
    // /// STEP.1: Decompose the Hamiltonian into MPO blocks
    vector<MPO> MPO_chain;
    MPO_chain = generate_MPO_chain(L, "XXZ_" + BC, S, para.J_list, 1.0, 0);
    string Jdis, Dim;
    /// create folder in order to save data
    // string file, dis, dim, folder, file_name, file_name1, file_name2, file_nameS;
    if (J < 1.0 && J < 0.1)
        Jdis = "00" + to_string( (int)(round(J*100)) );
    else if (J < 1.0 && J >= 0.1)
        Jdis = "0" +  to_string( (int)(round(J*100)) ); 
    else if (J >= 1.0)
        Jdis = to_string( (int)(round(J*100)) );
    
    if (D < 1.0 && D < 0.1)
        Dim = "00" + to_string( (int)(round(D*100)) );
    else if (D < 1.0 && D >= 0.1)
        Dim = "0" + to_string( (int)(round(D*100)) );
    else if (D >= 1.0)
        Dim = to_string( (int)(round(D*100)) );

    string folder = group_path;
    folder = folder + "/data_random/" + BC + "/Jdis" + Jdis + "/Dim" + Dim + "/L" + to_string(L) + "_P" + to_string(Pdis) + "_m" + to_string(chi) + "_" + to_string(sample);
    data.message += folder + "\nSpin" + to_string(S) + "\nSeed:" + to_string(seed);

    // do
    // {
    //     Jlist(para, data);
    //     cout << dimer(abs(sum(data.J_list,1)),abs(sum(data.J_list,0)))<<endl;
    // }
    // while(dimer(abs(sum(data.J_list,1)),abs(sum(data.J_list,0)))>dimerization);
    //     // cout << data.J_list[0];

    // cout << sum(data.J_list,1) << endl;
    // cout << sum(data.J_list,0) << endl;
    // cout << dimer(abs(sum(data.J_list,1)),abs(sum(data.J_list,0)));


    /// return: TTN(w_up and w_loc) and energy spectrum of top tensor
    vector<uni10::UniTensor<double> > w_up;      // w_up is isometry tensor = VT
    vector<int> w_loc;    
    // vector<double> rgJlist = data.rgJlist;
    // vector<double> En = data.energy;                 // J_list will earse to one, and return ground energy.
    for(int i = 0; i<para.J_list.size();i++)
    {
        data.J_list.push_back(para.J_list[i]);
    }
    bool info = 1;                               // True; if tSDRG can not find non-zero gap, info return 0, and stop this random seed.
    bool save_RG_info = 0;                       // save gaps at RG stage 
    // cout << data.message;
    tSDRG(MPO_chain, data.J_list, data.energy, w_up, w_loc, chi, to_string(J), Pdis, sample, save_RG_info, info);

    string str = "mkdir -p " + folder;
    const char *mkdir = str.c_str();
    const int dir_err = system(mkdir);
    if (dir_err == -1)
    {
        cout << "Error creating directory!" << endl;
        exit(1);
    }

    /// check info if can not RG_J
    if (info == 0)
    {
        cout << "random seed " + to_string(seed)  + " died (can not find non-zero gap) " << endl;
        return;
    }
    else
    {   
        data.message += ("\nfinish in " + folder + "\n");
    }

    //string top1 = Decision_tree(w_loc, true);

    /// create isometry of other part
    vector<uni10::UniTensor<double> > w_down;    // w_down
    uni10::UniTensor<double> kara;
    w_down.assign(L-1, kara);
    for (int i = 0; i < w_up.size(); i++)
    {
        w_down[i] = w_up[i];
        uni10::Permute(w_down[i], {-3, -1, 1}, 2, uni10::INPLACE);
    }

    /// save TTN; Don't do this. Your HDD will be fill with TTN
    /*file = folder;
    for (int i = 0; i < w_up.size(); i++)
    {
        file = folder + "/w_up" + to_string(i);
        w_up[i].Save(file);
    }*/

    /// save disorder coupling J list 
    vector<double> corr12;            // corr <S1><S2>
    string file;
    file = folder + "/J_list.csv";
    ofstream fout(file);              // == fout.open(file);
    if (!fout)
    {
        ostringstream err;
        err << "Error: Fail to save (maybe need mkdir " << file << ")";
        throw runtime_error(err.str());
    }
    for (int i = 0; i < para.J_list.size(); i++)
    {
        fout << setprecision(16) << para.J_list[i] << endl;
        corr12.push_back(Correlation_St(i, w_up, w_down, w_loc) );
    }
    fout.flush();
    fout.close();

    file = folder + "/RG_J_list.csv";
    fout.open(file);             // == fout.open(file);
    if (!fout)
    {
        ostringstream err;
        err << "Error: Fail to save (maybe need mkdir " << file << ")";
        throw runtime_error(err.str());
    }
    for (int i = 0; i < data.J_list.size(); i++)
    {
        fout << setprecision(16) << data.J_list[i] << endl;
    }
    fout.flush();
    fout.close();

    /// save merge order
    file = folder + "/w_loc.csv";
    fout.open(file);
    if (!fout)
    {
        ostringstream err;
        err << "Error: Fail to save (maybe need mkdir " << file << ")";
        throw runtime_error(err.str());
    }
    for (int i = 0; i < w_loc.size(); i++)
    {
        fout << w_loc[i] << endl;
        data.w_loc += to_string(w_loc[i]);
    }
    fout.flush();
    fout.close();

    /// save ground energy
    file = folder + "/energy.csv";
    fout.open(file);
    if (!fout)
    {
        ostringstream err;
        err << "Error: Fail to save (maybe need mkdir " << file << ")";
        throw runtime_error(err.str());
    }
    fout << "energy" << endl;
    for (int i=0; i<data.energy.size(); i++)
    {
        fout << setprecision(16) << data.energy[i] << endl;
        // data.energy (En[i]);
    }
    fout.flush();
    fout.close();
    string top1 = Decision_tree(w_loc, false);
    
    /// bulk correlation and string order parameter print
    double corr, corr1 ,corr2, sop;
    string file_name1 = folder + "/L" + to_string(L) + "_P" + to_string(Pdis) + "_m" + to_string(chi) + "_" + to_string(sample) + "_corr1.csv";
    string file_name2 = folder + "/L" + to_string(L) + "_P" + to_string(Pdis) + "_m" + to_string(chi) + "_" + to_string(sample) + "_corr2.csv";
    string file_nameS = folder + "/L" + to_string(L) + "_P" + to_string(Pdis) + "_m" + to_string(chi) + "_" + to_string(sample) + "_string.csv";
    ofstream fout1(file_name1);
    ofstream fout2(file_name2);
    ofstream foutS(file_nameS);
    fout1 << "x1,x2,corr" << endl;
    fout2 << "x1,x2,corr" << endl;
    foutS << "x1,x2,corr" << endl;
    int site1;
    int site2;
    int r;
    /// TODO: for OBC. Now is good for PBC.
    for (site1 = 0; site1 < L-1; site1 += 1)
    {
        int nn;
        if (site1 == 0)
            nn = 1;
        else
            nn = 10;

        for (site2 = site1+nn; site2 < L; site2 += 1)
        {
            r = site2 - site1;
            //cout << r << endl;
            if (r <= L/2)
            {
                //cout << "TEST: " << site1 << " & " << site2 << endl;
                // corr = Correlation_StSt(site1, site2, w_up, w_down, w_loc);
                // corr1 = corr12[site1];
                // corr2 = corr12[site2];

                // fout1 << setprecision(16) << site1 << "," << site2 << "," << corr << endl;
                // fout2 << setprecision(16) << site1 << "," << site2 << "," << corr - corr1*corr2 << endl;

                if (r == L/2)
                {
                    corr = Correlation_StSt(site1, site2, w_up, w_down, w_loc);
                    corr1 = corr12[site1];
                    corr2 = corr12[site2];
                    data.corr1 += (to_string(site1) + "," + to_string(site2) + "," + to_string(corr) + ";");
                    data.corr2 += (to_string(site1) + "," + to_string(site2) + "," + to_string(corr - corr1*corr2)+ ";");
                    fout1 << setprecision(16) << site1 << "," << site2 << "," << corr << endl;
                    fout2 << setprecision(16) << site1 << "," << site2 << "," << corr - corr1*corr2 << endl;

                    sop = Correlation_String(site1, site2, w_up, w_down, w_loc);
                    foutS << setprecision(16) << site1 << "," << site2 << "," << sop << endl;
                }
            }
        }
    }
    fout1.flush();
    fout2.flush();
    foutS.flush();
    fout1.close();
    fout2.close();
    foutS.close();

    /// save twist order parameter
    file = folder + "/" + to_string(sample) + "_seed.csv";
    fout.open(file);
    if (!fout)
    {
        ostringstream err;
        err << "Error: Fail to save (maybe need mkdir " << file << ")";
        throw runtime_error(err.str());
    }
    fout << "seed" << endl;
    fout << setprecision(16) << data.seed << endl;
    fout.flush();
    fout.close();

    /// save twist order parameter
    file = folder + "/dimerization.csv";
    fout.open(file);
    if (!fout)
    {
        ostringstream err;
        err << "Error: Fail to save (maybe need mkdir " << file << ")";
        throw runtime_error(err.str());
    }
    fout << "dimerization" << endl;
    fout << setprecision(16) << s_tempt << endl;
    fout.flush();
    fout.close();

    /// save twist order parameter
    file = folder + "/ZL.csv";
    fout.open(file);
    if (!fout)
    {
        ostringstream err;
        err << "Error: Fail to save (maybe need mkdir " << file << ")";
        throw runtime_error(err.str());
    }
    fout << "ZL" << endl;
    double ZL = Correlation_ZL(w_up, w_down, w_loc);
    fout << setprecision(16) << ZL << endl;
    data.ZL = ZL;
    fout.flush();
    fout.close();

    cout << (data.message += "ZL:" + to_string(data.ZL) + "\n\n");

}

void errMsg(char *arg) 
{
    cerr << "Usage: " << arg << " [options]" << endl;
    cerr << "Need 9-parameter:" << endl;
    cerr << "./job.exe <system size> <keep state of RG procedure> <Prob distribution> <disorder> <dimerization> <algo> <seed1> <seed2>\n" << endl;
    cerr << "Example:" << endl;
    cerr << "./job.exe 32 8 10 0.1 0.1 PBC 1 1\n" << endl;
}

int main(int argc, char *argv[])
{
    int L;                      // system size
    int chi;                    // keep state of isometry
    string BC;                  // boundary condition
    int Pdis;                   // model of random variable disturbution
    double Jdis;                // J-coupling disorder strength
    double Dim;			        // Dimerization constant
    int seed1;                  // random seed number in order to repeat data
    int seed2;                  // random seed number in order to repeat data
    double S      = 1.5;        // spin dimension
    double Jz     = 1.0;        // XXZ model
    double h      = 0.0;        // XXZ model
    string filePath;
    stringstream(argv[1]) >> filePath;

    // for(int i=0; i < parameter.size(); i++)
    // {
    //     cout << parameter[i].first << ", " << parameter[i].second << "\n";
    // }
    // cout << parameter[0].second;
    cout << filePath <<endl;
    seed1 = stoi(argv[2]);
    seed2 = stoi(argv[3]);

    for (int i = seed1; i <= seed2; i++) 
    {
        datalist dlist = {};
        paralist plist = {};
        vector<pair<string, string>> parameter;
        parameterRead(filePath, parameter);
        parameterSet(plist, parameter);
        plist.sample = i;
        plist.spin = S;
        tSDRG_XXZ(plist, dlist);
    }

    return 0;
}

