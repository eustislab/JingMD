load matlab.mat
wavenumber=1e7./wavelength
peak1=wavelength(find(gaussian1==max(gaussian1)))
f1=4.39e-9.*trapz(wavenumber,gaussian1)
peak2=wavelength(find(gaussian2==max(gaussian2)))
f2=4.39e-9.*trapz(wavenumber,gaussian2)
peak3=wavelength(find(gaussian3==max(gaussian3)))
f3=4.39e-9.*trapz(wavenumber,gaussian3)
peak4=wavelength(find(gaussian4==max(gaussian4)))
f4=4.39e-9.*trapz(wavenumber,gaussian4)
array=[f1,peak1,f2,peak2,f3,peak3,f4,peak4]
plot(wavelength,epsilon,wavelength, gaussian3, wavelength, gaussian1,wavelength, gaussian4,wavelength, gaussian2,'LineWidth',2)
title('Absorption spectrum of aniline in water'), ylabel('molar absorptivity (M-1cm-1)'), xlabel('Wavelength (nm)')
legend('Absorption spectrum','Underlying Gaussian 1','Underlying Gaussian 2','Underlying Gaussian 3','Underlying Gaussian 4')
xlim([200 350])
set(gca,'fontsize', 14)
orient landscape
print('-dpdf', 'UVFromFitykWavelength','-fillpage')