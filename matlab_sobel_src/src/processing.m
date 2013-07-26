function output=processing(fname_in,fname_out, option)

im_in=imread(fname_in);

fprintf('option: %g\n',option);

if option
	im_out=edge(im_in,'canny');
else
	im_out=edge(im_in,'sobel');
end


imwrite(im_out,fname_out);

%exit code
output=1;