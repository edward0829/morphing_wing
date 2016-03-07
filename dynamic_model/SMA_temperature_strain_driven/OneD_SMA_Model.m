function [sigma, MVF, T, eps_t]=OneD_SMA_Model(k, eps_current, T_0, T_final, MVF_init, eps_t_0, sigma_0, n, to_plot) %k, T_inp, eps_i,
% Modified Edwins original code to calculate just for a given T and eps
% Ideal: [sigma, MVF]=OneD_SMA_Model(T_inp, esp_inp)
%Inputs:
%         - k: current iteration of epsilon
%         - T_inp: [T0; Tmax [;T_final]]
%         - eps_i: current SMA strain
%         - n: Maximum Number of increments n per loading step
%         - plot: 'True' or 'False'


% Initializing environment
%clear all; close all; clc

%--------------------------------------------------------------------------
% INPUTS
%--------------------------------------------------------------------------


% INPUT:
% If list with three components:
% Temperature and strain at the start and at the ends of each loading step
% Linear increments strain and temperature loading step assumed
% If list with two components:
% Temperature and strain at the start and at the ends of heating
% Linear increments strain and temperature loading step assumed

% MATERIAL PARAMETERS (Structure: P)
% Young's Modulus for Austenite and Martensite 
P.E_A = 60E9;
P.E_M = 60E9;
% Transformation temperatures (M:Martensite, A:
% Austenite), (s:start,f:final)
P.M_s = 333.;
P.M_f = 220;
P.A_s = 274.;
P.A_f = 370.;

% Slopes of transformation boundarings into austenite (C_A) and
% martensite (C_M) at Calibration Stress 
P.C_A = 7.8E6;
P.C_M = 7.3e6;

% Maximum and minimum transformation strain
P.H_min = 0.00;
P.H_sat = 0.047;

P.k = 0.021E-6;
P.sig_crit = 140E6;

% Coefficient of thermal expansion
P.alpha = 10E-5;

% Smoothn hardening parameters 
% NOTE: smoothness parameters must be 1 for explicit integration scheme
P.n1 = 0.06; %0.618;
P.n2 = 0.06; %0.313;
P.n3 = 0.06; %0.759;
P.n4 = 0.06; %0.358;

% Algorithmic delta for modified smooth hardening function
P.delta=1e-5;

% Calibration Stress
P.sig_cal=300E6;

% Tolerance for change in MVF during implicit iteration
P.MVF_tolerance=1e-8;

% Generate strain and temperature states at each increment
%T: Temperature
if k == 2
  T_inp = [T_0; T_final];
    for i = 1:(size(T_inp,1)-1)
        if i == 1
            T = linspace(T_inp(i), T_inp(i+1), n)';
        else     
            T = [T; linspace(T_inp(i), T_inp(i+1),n)'];
        end
    end
else
    load('data.mat', 'T')
end
% eps: Strain
% if first iteration create list, otherwise load previous and update it
if k == 2
    eps = zeros(n,1);
    eps(1) = eps_current;
else
    load('data.mat', 'eps')
end
eps(k) = eps_current;


% Elastic Prediction Check
elastic_check = 'N';

% Integration Scheme
integration_scheme = 'I';

[sigma,MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model( k, T, eps, P, elastic_check, integration_scheme, MVF_init, eps_t_0, sigma_0 );

if strcmp(to_plot,'True')
    figure()
    box on 
    plot(eps,sigma,'b','LineWidth',1.5)
    xlabel('Strain')
    ylabel('Stress (MPa)')
    title('One D SMA Models')
    set(gca,'FontName','Times New Roman','fontsize', 20,'linewidth',1.15)
    set(gca,'XMinorTick','on','YMinorTick','on')
    set(gca,'ticklength',3*get(gca,'ticklength'))

    figure()
    box on 
    plot(T,sigma,'b','LineWidth',1.5)
    xlabel('Temperature')
    ylabel('Stress (MPa)')
    title('One D SMA Models')
    set(gca,'FontName','Times New Roman','fontsize', 20,'linewidth',1.15)
    set(gca,'XMinorTick','on','YMinorTick','on')
    set(gca,'ticklength',3*get(gca,'ticklength'))
    
    figure()
    box on 
    plot(T,eps_t,'b','LineWidth',1.5)
    xlabel('Temperature')
    ylabel('Transformation strain)')
    title('One D SMA Models')
    set(gca,'FontName','Times New Roman','fontsize', 20,'linewidth',1.15)
    set(gca,'XMinorTick','on','YMinorTick','on')
    set(gca,'ticklength',3*get(gca,'ticklength'))

    figure()
    box on 
    plot(T, MVF,'b','LineWidth',1.5)
    xlabel('Temperature')
    ylabel('Martensitic volume fraction')
    title('One D SMA Models')
    set(gca,'FontName','Times New Roman','fontsize', 20,'linewidth',1.15)
    set(gca,'XMinorTick','on','YMinorTick','on')
    set(gca,'ticklength',3*get(gca,'ticklength'))

    figure()
    box on 
    plot(sigma, MVF,'b','LineWidth',1.5)
    xlabel('Stess (MPa)')
    ylabel('Martensitic volume fraction')
    title('One D SMA Models')
    set(gca,'FontName','Times New Roman','fontsize', 20,'linewidth',1.15)
    set(gca,'XMinorTick','on','YMinorTick','on')
    set(gca,'ticklength',3*get(gca,'ticklength'))
end
