// This file is part of babel4iphone.

// Copyright (C) 2009 Giovanni Amati <amatig@gmail.com>

// babel4iphone is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// babel4iphone is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with babel4iphone.  If not, see <http://www.gnu.org/licenses/>.


#ifndef __CORE_FUNCTION_H__
#define __CORE_FUNCTION_H__

@interface CoreFunctions : NSObject
{

}

+(int) scaleHP:(float)sHP baseHP:(float)bHP scaleHPxXx:(float)sHPxXx level:(int)l;
+(int) scaleHP:(float)sHP baseHP:(float)bHP scaleHPxXx:(float)sHPxXx level:(int)l job:(NSString *)j;
+(int) scaleHP:(float)sHP baseHP:(float)bHP suplevel:(int)sl supjob:(NSString *)sj;
+(int) scaleMP:(float)sMP baseMP:(float)bMP levelMP:(int)lm;
+(int) scaleMP:(float)sMP baseMP:(float)bMP levelMP:(int)lm level:(int)l job:(NSString *)j;
+(int) scaleMP:(float)sMP baseMP:(float)bMP suplevel:(int)sl supjob:(NSString *)sj;
+(int) scaleSTATS:(float)sSTATS baseSTATS:(float)bSTATS level:(int)l;

@end

#endif
