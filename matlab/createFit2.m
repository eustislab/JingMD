function [pd1,pd2,pd3,pd4,pd5] = createFit2(arg_1,arg_2,arg_3,arg_4,arg_5)
%CREATEFIT    Create plot of datasets and fits
%   [PD1,PD2,PD3,PD4,PD5] = CREATEFIT(ARG_1,ARG_2,ARG_3,ARG_4,ARG_5)
%   Creates a plot, similar to the plot in the main distribution fitting
%   window, using the data that you provide as input.  You can
%   apply this function to the same data you used with dfittool
%   or with different data.  You may want to edit the function to
%   customize the code and this help message.
%
%   Number of datasets:  5
%   Number of fits:  5
%
%   See also FITDIST.

% This function was automatically generated on 23-Nov-2015 12:50:11

% Output fitted probablility distributions: PD1,PD2,PD3,PD4,PD5

% Data from dataset "S1(:,1) data":
%    Y = arg_1 (originally S1(:,1))

% Data from dataset "S2(:,1) data":
%    Y = arg_2 (originally S2(:,1))

% Data from dataset "S3(:,1) data":
%    Y = arg_3 (originally S3(:,1))

% Data from dataset "S4(:,1) data":
%    Y = arg_4 (originally S4(:,1))

% Data from dataset "S5(:,1) data":
%    Y = arg_5 (originally S5(:,1))

% Force all inputs to be column vectors
arg_1 = arg_1(:);
arg_2 = arg_2(:);
arg_3 = arg_3(:);
arg_4 = arg_4(:);
arg_5 = arg_5(:);

% Prepare figure
clf;
hold on;
LegHandles = []; LegText = {};


% --- Plot data originally in dataset "S1(:,1) data"
[CdfF,CdfX] = ecdf(arg_1,'Function','cdf');  % compute empirical cdf
BinInfo.rule = 5;
BinInfo.width = 0.001;
BinInfo.placementRule = 1;
[~,BinEdge] = internal.stats.histbins(arg_1,[],[],BinInfo,CdfF,CdfX);
[BinHeight,BinCenter] = ecdfhist(CdfF,CdfX,'edges',BinEdge);
hLine = bar(BinCenter,BinHeight,'hist');
set(hLine,'FaceColor','none','EdgeColor',[0.333333 0 0.666667],...
    'LineStyle','-', 'LineWidth',1);
xlabel('Data');
ylabel('Density')
LegHandles(end+1) = hLine;
LegText{end+1} = 'S1(:,1) data';

% --- Plot data originally in dataset "S2(:,1) data"
[CdfF,CdfX] = ecdf(arg_2,'Function','cdf');  % compute empirical cdf
BinInfo.rule = 5;
BinInfo.width = 0.001;
BinInfo.placementRule = 1;
[~,BinEdge] = internal.stats.histbins(arg_2,[],[],BinInfo,CdfF,CdfX);
[BinHeight,BinCenter] = ecdfhist(CdfF,CdfX,'edges',BinEdge);
hLine = bar(BinCenter,BinHeight,'hist');
set(hLine,'FaceColor','none','EdgeColor',[0.333333 0.666667 0],...
    'LineStyle','-', 'LineWidth',1);
xlabel('Data');
ylabel('Density')
LegHandles(end+1) = hLine;
LegText{end+1} = 'S2(:,1) data';

% --- Plot data originally in dataset "S3(:,1) data"
[CdfF,CdfX] = ecdf(arg_3,'Function','cdf');  % compute empirical cdf
BinInfo.rule = 5;
BinInfo.width = 0.001;
BinInfo.placementRule = 1;
[~,BinEdge] = internal.stats.histbins(arg_3,[],[],BinInfo,CdfF,CdfX);
[BinHeight,BinCenter] = ecdfhist(CdfF,CdfX,'edges',BinEdge);
hLine = bar(BinCenter,BinHeight,'hist');
set(hLine,'FaceColor','none','EdgeColor',[0 0 0],...
    'LineStyle','-', 'LineWidth',1);
xlabel('Data');
ylabel('Density')
LegHandles(end+1) = hLine;
LegText{end+1} = 'S3(:,1) data';

% --- Plot data originally in dataset "S4(:,1) data"
[CdfF,CdfX] = ecdf(arg_4,'Function','cdf');  % compute empirical cdf
BinInfo.rule = 5;
BinInfo.width = 0.001;
BinInfo.placementRule = 1;
[~,BinEdge] = internal.stats.histbins(arg_4,[],[],BinInfo,CdfF,CdfX);
[BinHeight,BinCenter] = ecdfhist(CdfF,CdfX,'edges',BinEdge);
hLine = bar(BinCenter,BinHeight,'hist');
set(hLine,'FaceColor','none','EdgeColor',[0.333333 1 0.666667],...
    'LineStyle','-', 'LineWidth',1);
xlabel('Data');
ylabel('Density')
LegHandles(end+1) = hLine;
LegText{end+1} = 'S4(:,1) data';

% --- Plot data originally in dataset "S5(:,1) data"
[CdfF,CdfX] = ecdf(arg_5,'Function','cdf');  % compute empirical cdf
BinInfo.rule = 5;
BinInfo.width = 0.001;
BinInfo.placementRule = 1;
[~,BinEdge] = internal.stats.histbins(arg_5,[],[],BinInfo,CdfF,CdfX);
[BinHeight,BinCenter] = ecdfhist(CdfF,CdfX,'edges',BinEdge);
hLine = bar(BinCenter,BinHeight,'hist');
set(hLine,'FaceColor','none','EdgeColor',[0 0.333333 0.666667],...
    'LineStyle','-', 'LineWidth',1);
xlabel('Data');
ylabel('Density')
LegHandles(end+1) = hLine;
LegText{end+1} = 'S5(:,1) data';

% Create grid where function will be computed
XLim = get(gca,'XLim');
XLim = XLim + [-1 1] * 0.01 * diff(XLim);
XGrid = linspace(XLim(1),XLim(2),100);


% --- Create fit "fit 5"

% Fit this distribution to get parameter values
% To use parameter estimates from the original fit:
%     pd1 = ProbDistUnivParam('normal',[ 6.153529283417, 0.1760606585338])
pd1 = fitdist(arg_5, 'normal');
YPlot = pdf(pd1,XGrid);
hLine = plot(XGrid,YPlot,'Color',[1 0 0],...
    'LineStyle','-', 'LineWidth',2,...
    'Marker','none', 'MarkerSize',6);
LegHandles(end+1) = hLine;
LegText{end+1} = 'fit 5';

% --- Create fit "fit 2"

% Fit this distribution to get parameter values
% To use parameter estimates from the original fit:
%     pd2 = ProbDistUnivParam('normal',[ 5.355870740704, 0.1617364029781])
pd2 = fitdist(arg_2, 'normal');
YPlot = pdf(pd2,XGrid);
hLine = plot(XGrid,YPlot,'Color',[0 0 1],...
    'LineStyle','-', 'LineWidth',2,...
    'Marker','none', 'MarkerSize',6);
LegHandles(end+1) = hLine;
LegText{end+1} = 'fit 2';

% --- Create fit "fit 3"

% Fit this distribution to get parameter values
% To use parameter estimates from the original fit:
%     pd3 = ProbDistUnivParam('normal',[ 5.593928310553, 0.1400113829092])
pd3 = fitdist(arg_3, 'normal');
YPlot = pdf(pd3,XGrid);
hLine = plot(XGrid,YPlot,'Color',[0.666667 0.333333 0],...
    'LineStyle','-', 'LineWidth',2,...
    'Marker','none', 'MarkerSize',6);
LegHandles(end+1) = hLine;
LegText{end+1} = 'fit 3';

% --- Create fit "fit 4"

% Fit this distribution to get parameter values
% To use parameter estimates from the original fit:
%     pd4 = ProbDistUnivParam('normal',[ 5.837371293467, 0.1872150864263])
pd4 = fitdist(arg_4, 'normal');
YPlot = pdf(pd4,XGrid);
hLine = plot(XGrid,YPlot,'Color',[0.333333 0.333333 0.333333],...
    'LineStyle','-', 'LineWidth',2,...
    'Marker','none', 'MarkerSize',6);
LegHandles(end+1) = hLine;
LegText{end+1} = 'fit 4';

% --- Create fit "fit 1"

% Fit this distribution to get parameter values
% To use parameter estimates from the original fit:
%     pd5 = ProbDistUnivParam('normal',[ 4.862904692462, 0.1352429073038])
pd5 = fitdist(arg_1, 'normal');
YPlot = pdf(pd5,XGrid);
hLine = plot(XGrid,YPlot,'Color',[1 0 1],...
    'LineStyle','-', 'LineWidth',2,...
    'Marker','none', 'MarkerSize',6);
LegHandles(end+1) = hLine;
LegText{end+1} = 'fit 1';

% Adjust figure
box on;
hold off;

% Create legend from accumulated handles and labels
hLegend = legend(LegHandles,LegText,'Orientation', 'vertical', 'FontSize', 9, 'Location', 'northeast');
set(hLegend,'Interpreter','none');
print('-dpng','fPlot')
