
clear;
close all hidden;

% Get images

orgS1 = imread("Seattle 1.jpg");
orgS2 = imread("Seattle 2.jpg");

binS1 = imbinarize(orgS1);
binS2 = imbinarize(orgS2);

histOrg1 = imhist(orgS1);
histOrg2 = imhist(orgS2);
histBin1 = imhist(binS1);
histBin2 = imhist(binS2);

% Display these as images

figure;
subplot(2,4,1); imshow(orgS1); title("Seattle 1");
subplot(2,4,2); imshow(binS1); title("Bin Seattle 1");
subplot(2,4,3); imshow(orgS2); title("Seattle 2");
subplot(2,4,4); imshow(binS2); title("Bin Seattle 2");
subplot(2,4,5); bar(histOrg1); title("Seattle 1 Hist");
subplot(2,4,6); bar(histBin1); title("Bin Seattle 1 Hist");
subplot(2,4,7); bar(histOrg2); title("Seattle 2 Hist");
subplot(2,4,8); bar(histBin2); title("Bin Seattle 2 Hist");

% Local thresholding method for first image

s1Thresh = localThreshold(orgS1,540,1900,30,0.7);

% Some post processing 

SE = strel("square",2);

s1Processed = imopen(s1Thresh,SE);
s1Processed = bwmorph(s1Processed,"thin",1);

figure;
subplot(1,2,1); imshow(s1Thresh); title("Seattle 1");
subplot(1,2,2); imshow(s1Processed); title("Processed");

% Local thresholding for second image

s2Thresh = localThreshold(orgS2,800,1550,15,0.8);

% Some post processing

s2Processed = imopen(s2Thresh,SE);
s2Processed = bwmorph(s2Processed,"thin",1);

figure;
subplot(1,2,1); imshow(s2Thresh); title("Seattle 2");
subplot(1,2,2); imshow(s2Processed); title("Processed");

return;



function output = localThreshold(processImage, imageTop, imageBot, windowSize, thresholdFactor)
    
    output = processImage;

    maxR = height(output);
    maxC = width(output);

    topR = 1;
    topC = 1;

    botR = windowSize;
    botC = windowSize;

    while topR <= maxR

        % If the bottom of the window is in the image, cut off at the image
        if botR > imageTop && botR < imageBot
            botR = imageTop;
        end 

        % If the row of the window goes off the image, cut off extra r's
        if botR > maxR
            botR = maxR;
        end

        if topR > imageTop && topR < imageBot
            % Deletes image
            for r = imageTop:imageBot
                for c = 1:maxC
                    output(r,c) = 1;
                end
            end

            topR = imageBot + 1;
            botR = topR + windowSize -1;
        else

            while topC <= maxC
                
                % Get local average
                localMean = 0;
                totalPixels = 0;
    
                for r = topR:botR
                    for c = topC:botC
                        localMean = localMean + double(output(r,c));
                        totalPixels = totalPixels + 1;
                    end
                end
    
                localMean = localMean/totalPixels;
                T = localMean * thresholdFactor;
    
                % Threshold image region
                for r = topR:botR
                    for c = topC:botC
                        if output(r,c) < T
                            output(r,c) = 0;
                        else
                            output(r,c) = 1;
                        end
                    end
                end

                % Change c values

                topC = botC + 1;
                botC = topC + windowSize - 1;

                % If the column of the window goes off the image, cut off extra c's
                if botC > maxC
                    botC = maxC;
                end

            end
            
            % Reset topC and botC
            topC = 1;
            botC = windowSize;
            
        end

        % Increase topR and botR
        topR = botR + 1;
        botR = topR + windowSize - 1;
        
    end

    output = logical(output);

end

