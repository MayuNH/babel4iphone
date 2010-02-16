//
//  GameLayer.h
//  Genoma
//
//  Created by Giovanni Amati on 08/10/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "cocos2d.h"

@interface GameLayer : CCLayer
{

}

-(void) addMyCharacter:(NSArray *)attr position:(int)p;
-(void) addEnemyCharacter:(NSArray *)attr position:(int)p;

@end