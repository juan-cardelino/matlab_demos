function gauss(filename_in, filename_out, sigma)

if isdeployed
sigma = str2double(sigma);
end

% read image
im = imread(filename_in);

% create filter
h = create_filter(sigma);

% apply filter
im = imfilter(im,h);

% write result
imwrite(im, filename_out);
