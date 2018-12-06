function pts = calc_circle_int(Ra, Rb, Ca, Cb)
    xa = Ca(1);
    ya = Ca(2);
    xb = Cb(1);
    yb = Cb(2);
    a = Ra;
    b = Rb;

    
    x1 = ((-a^2)*xa + b^2*xa + xa^3 + a^2*xb - b^2*xb - xa^2*xb - xa*xb^2 + xb^3 + xa*ya^2 + xb*ya^2 - 2*xa*ya*yb - 2*xb*ya*yb + xa*yb^2 + xb*yb^2 - ...
        sqrt(-(ya - yb)^2)*(a^4 + (-b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)^2 - 2*a^2*(b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)))/(2*(xa^2 - 2*xa*xb + xb^2 + (ya - yb)^2));
    
    y1 = (1/(2*(xa^2 - 2*xa*xb + xb^2 + (ya - yb)^2)*(ya - yb)))*((-a^2)*ya^2 + b^2*ya^2 + xa^2*ya^2 - 2*xa*xb*ya^2 + xb^2*ya^2 + ya^4 + 2*a^2*ya*yb - 2*b^2*ya*yb - 2*ya^3*yb - a^2*yb^2 + b^2*yb^2 - xa^2*yb^2 + 2*xa*xb*yb^2 - xb^2*yb^2 + 2*ya*yb^3 - yb^4 + ...
      xa*sqrt(-(ya - yb)^2)*(a^4 + (-b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)^2 - 2*a^2*(b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)) - ...
      xb*sqrt(-(ya - yb)^2)*(a^4 + (-b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)^2 - 2*a^2*(b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)));
    
    x2 = ((-a^2)*xa + b^2*xa + xa^3 + a^2*xb - b^2*xb - xa^2*xb - xa*xb^2 + xb^3 + xa*ya^2 + xb*ya^2 - 2*xa*ya*yb - 2*xb*ya*yb + xa*yb^2 + xb*yb^2 + ...
      sqrt(-(ya - yb)^2)*(a^4 + (-b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)^2 - 2*a^2*(b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)))/(2*(xa^2 - 2*xa*xb + xb^2 + (ya - yb)^2));
  
    y2 = (1/(2*(xa^2 - 2*xa*xb + xb^2 + (ya - yb)^2)*(ya - yb)))*((-a^2)*ya^2 + b^2*ya^2 + xa^2*ya^2 - 2*xa*xb*ya^2 + xb^2*ya^2 + ya^4 + 2*a^2*ya*yb - 2*b^2*ya*yb - 2*ya^3*yb - a^2*yb^2 + b^2*yb^2 - xa^2*yb^2 + 2*xa*xb*yb^2 - xb^2*yb^2 + 2*ya*yb^3 - yb^4 - ...
      xa*sqrt(-(ya - yb)^2)*(a^4 + (-b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)^2 - 2*a^2*(b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)) + ...
      xb*sqrt(-(ya - yb)^2)*(a^4 + (-b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)^2 - 2*a^2*(b^2 + xa^2 - 2*xa*xb + xb^2 + ya^2 - 2*ya*yb + yb^2)));
  
  pts = [x1, x2; y1, y2];
    
end
